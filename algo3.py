import sqlite3 as lite
import random
import re

db = lite.connect('employees2.db')
cur = db.cursor()
week = {}


class Week():
    
    def __init__(self):
        self.budget  = 415
        self.computeHours(self.budget)
        self.setMaxHours()
        self.buildSkeleton()
        self.fillSkeleton()
        #self.fitWeekplan()
        self.buffSchedule()
        for i in self.weekplan.keys():
            print(i, self.schedule[i])
    
    def computeHours(self, weekbudget):
        ''' Generate an daily hour budget based on the amount of hours available in a week.
        Reserves 2 shifts for Saturday and Sunday.'''
        self.weekplan = {}
        self.daybudget = (weekbudget-15)//7
        for day in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
            if day in ('sunday', 'saturday'):
                self.weekplan[day] = [self.daybudget + 7.5, 0]
            else:
                self.weekplan[day] = [self.daybudget, 0]
        return self.weekplan
    
    def setMaxHours(self):
        ''' Sets the max hours of every employee. Does not save to database.'''
        fts = []
        pts = []
        cur.execute('UPDATE employees SET maxhours = 37.5 WHERE position = 0')
        cur.execute('UPDATE employees SET maxhours = 37.5 WHERE position > 0 and position < 3')
        cur.execute('SELECT name FROM employees WHERE position = 0')
        for i in cur.fetchall():
            fts.append(40)
        cur.execute('SELECT name FROM employees WHERE position > 0 and position < 3')
        for i in cur.fetchall():
            fts.append(37.5)
        cur.execute('SELECT name FROM employees WHERE position = 2')
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
        
        cur.execute('UPDATE employees SET maxhours = {pt} WHERE position = 3'.\
                    format(pt=pthours)) 
        
    def buildSkeleton(self):
        ''' Fills in fundamental shifts'''
        self.schedule = {}
        for day in [i for i in self.weekplan.keys() if self.weekplan[i][-1] <= self.weekplan[i][0] - 7.5]:
            self.schedule[day] = {}
            for ms in [845, 1100, 1330]:
                self.scheduleworker(ms, day, 1, 7.5)
            for ms in [915]:
                self.scheduleworker(ms, day, 2, 7.5)
            for ms in [845, 1330]:
                self.scheduleworker(ms, day, 0, 7.5)
                
    def fillSkeleton(self):
        ''' Fills up the rest of a schedule'''
        for ss in [1330, 1100]:
            for day in [i for i in self.weekplan.keys() if self.weekplan[i][-1] <= self.weekplan[i][0] - 7.5]:
                self.scheduleworker(ss, day, 0, 7.5, check = '!=')
        for ss in [1630, '1100B']:
            for day in [i for i in self.weekplan.keys() if self.weekplan[i][-1] <= self.weekplan[i][0] - 5]:
                self.scheduleworker(ss, day, 0, 5, position = 3, check = '!=')
    
    def scheduleworker(self, shift, day, _type, hoursneeded, position = 'None', check = '='):
        ''' Does the dry work of scheduling an employee and updating their hours.'''
        worker = self.queryDatabase(day, _type, hoursneeded, position = position, check = check)
        if worker == None:
            self.queryDatabase(day, 3)
        try:
            if worker != 'None':
                self.schedule[day][shift] += worker
            else: pass
        except KeyError:
            if worker != 'None':
                self.schedule[day][shift] = worker 
            else: pass
        self.updateHours(worker, hoursneeded, day)
        
    def fitWeekplan(self):
        self.extrahours = 0
        for day in self.weekplan.keys():
            self.extrahours += self.weekplan[day][0] - self.weekplan[day][1]
            self.weekplan[day][0] = self.weekplan[day][1] 
    
    def buffSchedule(self):
        for ss in [1200, 1200, 1200]:
            for day in self.weekplan.keys():
                self.scheduleworker(ss, day, 0, 7.5, check = '!=')
        for ss in [1500, 1500, 1500]:
            for day in self.weekplan.keys():
                self.scheduleworker(ss, day, 0, 5, position = 3, check = '!=')
            
    def queryDatabase(self, day, _type, hoursneeded = 7.5, position = 'None', check = '='):
        '''Runs a query on database and returns a result'''
        if position == 'None':
            query = 'SELECT name FROM employees where %s = 1 and type %s %s and hours <= maxhours - %s' % (day, check, _type, hoursneeded) 
        else:
            query = 'SELECT name FROM employees WHERE %s = 1 and type %s %s and hours <= maxhours - %s and position = %s' % (day, check, _type, hoursneeded, position)      
        cur.execute(query)
        available = cur.fetchall()
        if len(available) == 0:
            if position == 'None':
                query = 'SELECT name FROM employees where %s = 1 and type %s %s and hours <= maxhours - %s' % (day, check, '3', hoursneeded)
                cur.execute(query)
                available = cur.fetchall()
            else:
                query = 'SELECT name FROM employees WHERE %s = 1 and type %s %s and hours <= maxhours - %s and position = %s' % (day, check, '3', hoursneeded, position)
                cur.execute(query)
                available = cur.fetchall()  
        try:
            worker = random.choice(available)
            worker = re.sub('[(),]', '', str(worker))
        except:
            worker = 'None'
        return worker

    def updateHours(self, worker, hoursworked, day):
        ''' Adds hours to employee. Temporarily writes to database.'''
        try:
            query = 'UPDATE employees SET hours = hours + %s WHERE name = %s' % (hoursworked, worker)
            cur.execute(query)
            query = 'UPDATE employees set %s = 0 WHERE name = %s' % (day, worker)
            cur.execute(query)
            x = True
        except:
            x = False
            
        if x == True:
            self.weekplan[day][-1] += hoursworked
            self.budget -= hoursworked
            