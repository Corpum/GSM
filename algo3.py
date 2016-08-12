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
    
    def computeHours(self, weekbudget):
        ''' Generate an daily hour budget based on the amount of hours available in a week.
        Reserves 2 shifts for Saturday and Sunday.'''
        self.weekplan = {}
        self.daybudget = (weekbudget-15)//7
        for day in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
            if day in ('sunday', 'monday'):
                self.weekplan[day] = self.daybudget + 7.5
            else:
                self.weekplan[day] = self.daybudget
        return self.weekplan
    
    def setMaxHours(self):
        ''' Sets the max hours of every employee. Does not save to database.'''
        fts = []
        pts = []
        cur.execute('UPDATE employees SET maxhours = 40 WHERE position = 0')
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
        for day in self.weekplan.keys():
            self.schedule[day] = {}
            for ms in [845, 1100, 1330]:
                cashier = self.queryDatabase(day, 1)
                if cashier == 'None':
                    cashier = self.queryDatabase(day, 3)
                self.schedule[day][ms] = cashier
                self.updateHours(cashier, 7.5, day)
            for ms in [915]:
                sorter = self.queryDatabase(day, 2)
                if sorter == 'None':
                    sorter = self.queryDatabase(day, 3)
                self.schedule[day][ms] = sorter
                self.updateHours(sorter, 7.5, day)
            for ms in [845, 1330]:
                manager = self.queryDatabase(day, 0)
                self.schedule[day][ms] += manager
                self.updateHours(manager, 7.5, day)
            
    def queryDatabase(self, day, _type, hoursneeded = 7.5):
        '''Runs a query on database and returns a result'''
        query = 'SELECT name FROM employees where %s = 1 and type = %s and hours <= maxhours - %s' % (day, _type, hoursneeded) 
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
        query = 'UPDATE employees SET hours = hours + %s WHERE name = %s' % (hoursworked, worker)
        cur.execute(query)
        query = 'UPDATE employees set %s = 0 WHERE name = %s' % (day, worker)
        cur.execute(query)