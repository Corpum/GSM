import sqlite3 as lite
import random
import re

db = lite.connect('stafflist.db')
cur = db.cursor()
week = {}


class Week():
    '''Create a schedule for Sunday - Monday'''
    def __init__(self):
        self.budget = 415
        self.computeHours()
        self.setMaxHours()
        self.buildSkeleton()
        self.fillSkeleton()
        # self.fitWeekplan()
        self.buffSchedule()

    def computeHours(self):
        ''' Generate an daily hour budget based on the amount of hours
        available in a week. Reserves 2 shifts for Saturday and sunday.'''
        self.schedule2 = {}
        self.weekplan = {}
        self.daybudget = (self.budget-15)//7
        for day in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday'):
            if day in ('sunday', 'saturday'):
                self.weekplan[day] = [self.daybudget + 7.5, 0]
            else:
                self.weekplan[day] = [self.daybudget, 0]
        return self.weekplan

    def setMaxHours(self):
        ''' Sets the max hours of every employee. Does not save to database.'''
        fts = []
        pts = []
        cur.execute('UPDATE staff SET maxhours = 37.5 WHERE position = 0')
        cur.execute('UPDATE staff SET maxhours = 37.5'
                    + ' WHERE position > 0 and position < 3')
        cur.execute('SELECT name FROM staff WHERE position = 0')
        for i in cur.fetchall():
            fts.append(40)
        cur.execute('SELECT name FROM staff WHERE position > 0'
                    + ' and position < 3')
        for i in cur.fetchall():
            fts.append(37.5)
        cur.execute('SELECT name FROM staff WHERE position = 2')
        for i in cur.fetchall():
            pts.append(1)
        pthours = (self.budget - sum(fts)) / len(pts)
        if pthours > 22.5:
            pthours = 22.5
        elif pthours > 20:
            pthours = 20
        elif pthours > 17.5:
            pthours = 17.5
        elif pthours > 15:
            pthours = 15
        else:
            print('Not enough hours for part-timers')

        cur.execute('UPDATE staff SET maxhours = {pt} WHERE position = 3'.
                    format(pt=pthours))

    def buildSkeleton(self):
        ''' Fills in fundamental shifts'''
        self.schedule = {}
        for day in [i for i in self.weekplan.keys()
                    if self.weekplan[i][-1] <= self.weekplan[i][0] - 7.5]:
            self.schedule[day] = {}
            for ms in [('8:45', '4:45', 7.5),
                       ('11:00', '7:00', 7.5),
                       ('1:30', '9:30', 7.5)]:
                self.scheduleworker(ms, day, 1, 7.5)
            for ms in [('9:15', '5:15', 7.5)]:
                self.scheduleworker(ms, day, 2, 7.5)
            for ms in [('8:45', '4:45', 7.5),
                       ('1:30', '9:30', 7.5)]:
                self.scheduleworker(ms, day, 0, 7.5)

    def fillSkeleton(self):
        ''' Fills up the rest of a schedule'''
        for ss in [('1:30', '9:30', 7.5),
                   ('11:00', '7:00', 7.5)]:
            for day in [i for i in self.weekplan.keys()
                        if self.weekplan[i][-1] <= self.weekplan[i][0] - 7.5]:
                self.scheduleworker(ss, day, 0, 7.5, check='!=')
        for ss in [('16:30', '9:30', 5), ('11:00', '4:00', 5)]:
            for day in [i for i in self.weekplan.keys()
                        if self.weekplan[i][-1] <= self.weekplan[i][0] - 5]:
                self.scheduleworker(ss, day, 0, 5, position=3, check='!=')

    def scheduleworker(self, shift, day, _type,
                       hoursneeded, position='None', check='='):
        '''Schedules an employee and updates their working hours.'''
        worker = self.queryDatabase(day, _type, hoursneeded,
                                    position=position, check=check)
        if worker is None:
            self.queryDatabase(day, 3)
        try:
            if worker != 'None':
                self.schedule[day][shift] += worker
            else:
                pass
        except KeyError:
            if worker != 'None':
                self.schedule[day][shift] = worker
            else:
                pass
        try:
            if worker != 'None':
                self.schedule2[worker].append([day, shift])
            else:
                pass
        except KeyError:
            if worker != 'None':
                self.schedule2[worker] = []
                self.schedule2[worker].append([day, shift])
            else:
                pass
        self.updateHours(worker, hoursneeded, day)

    def fitWeekplan(self):
        self.extrahours = 0
        for day in self.weekplan.keys():
            self.extrahours += self.weekplan[day][0] - self.weekplan[day][1]
            self.weekplan[day][0] = self.weekplan[day][1]

    def buffSchedule(self):
        for ss in [('12:00', '8:00', 7.5),
                   ('12:00', '8:00', 7.5),
                   ('12:00', '8:00', 7.5)]:
            for day in self.weekplan.keys():
                self.scheduleworker(ss, day, 0, 7.5, check='!=')
        for ss in [('3:00', '8:00', 5),
                   ('3:00', '8:00', 5),
                   ('3:00', '8:00', 5)]:
            for day in self.weekplan.keys():
                self.scheduleworker(ss, day, 0, 5, position=3, check='!=')

    def queryDatabase(self, day, _type, hoursneeded=7.5,
                      position='None', check='='):
        '''Runs a query on database and returns a result'''
        if position == 'None':
            query = (('SELECT name FROM staff where %s = 1'
                     + ' and type %s %s and hours <= maxhours - %s')
                     % (day, check, _type, hoursneeded))
        else:
            query = (('SELECT name FROM staff WHERE %s = 1'
                     + ' and type %s %s and hours <= maxhours - %s'
                     + ' and position=%s')
                     % (day, check, _type, hoursneeded, position))
        cur.execute(query)
        available = cur.fetchall()
        if len(available) == 0:
            if position == 'None':
                query = (('SELECT name FROM staff where %s = 1'
                         + ' and type %s %s and hours <= maxhours - %s')
                         % (day, check, '3', hoursneeded))
                cur.execute(query)
                available = cur.fetchall()
            else:
                query = (('SELECT name FROM staff WHERE %s = 1'
                         + ' and type %s %s and hours <= maxhours - %s'
                         + ' and position = %s')
                         % (day, check, '3', hoursneeded, position))
                cur.execute(query)
                available = cur.fetchall()
        try:
            worker = random.choice(available)
            worker = re.sub('[(),\']', '', str(worker))
        except:
            worker = 'None'
        return worker

    def updateHours(self, worker, hoursworked, day):
        ''' Adds hours to employee. Temporarily writes to database.'''
        try:
            params = (hoursworked, worker)
            cur.execute(('UPDATE staff'
                        + ' SET hours = hours + ? WHERE name = ?'), params)
        except ValueError:
            pass

        cur.execute(('UPDATE staff SET {} = 0 WHERE name = ?')
                    .format(day), (worker,))
        x = True

        if x:
            self.weekplan[day][-1] += hoursworked
            self.budget -= hoursworked
