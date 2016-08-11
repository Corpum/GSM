import sqlite3 as lite
import random


db = lite.connect('employees2.db')
cur = db.cursor()
week = {}


class Week():
    
    def __init__(self):
        self.computeHours(415)
    
    def computeHours(self, weekbudget):
        ''' Generate an daily hour budget based on the amount of hours available in a week.
        Reserves 2 shifts for Saturday and Sunday.'''
        self.weekplan = {}
        self.daybudget = (weekbudget-15)//7
        for day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
            if day in ('sunday', 'monday'):
                self.weekplan[day] = self.daybudget + 7.5
            else:
                self.weekplan[day] = self.daybudget
        return self.weekplan
        
    def buildSkeleton(self, employees):
        self.schedule = {}
        for day in self.weekplan.keys():
            for ms in (845, 915, 1100, 1330):
                worker = self.queryDatabase(day)
                
                
            
    def queryDatabase(self, day, *constraints):
        '''Runs a query on database and returns a result'''
        cur.execute('SELECT name FROM restrictions WHERE {dayf} = 1 and id > 3 and hours < '.\
                    format(dayf=day))
        return cur.fetchone()
    
    def updateHours(self, worker, hours):