import sqlite3 as lite
import random

db = lite.connect('employees.db')
cur = db.cursor()
managers = {}
fulltimers = {}
parttimers = {}
week = {}
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
class Workweek():
    def __init__(self):
        # load in database
        cur.execute('SELECT * FROM employees')
        rows = cur.fetchall()
        for i in rows:
            if i[2] == 0:
                managers[i[1]] = 0
            elif i[2] == 1:
                fulltimers[i[1]] = 0
            elif i[2] == 2:
                parttimers[i[1]] = 0
        self.loadweek(days)
        self.fillmanagers()
    def loadweek(self, days):
        for i in days:
            week[i] = {'8:45':[], '11:00':[], '1:30':[]}
    
    def updatehours(self,position, name):
        position[name] += 8
        for name in position:
            if position[name] >= 40:
                try:
                    self.mavail.remove(name)
                except ValueError:
                    pass
    def fillmanagers(self):
        self.mavail = []
        for i in managers:
            self.mavail.append(i)
        for day in week.keys():
            daily = list(self.mavail)
            openmanager = random.choice(daily)
            week[day]['8:45'].append(openmanager)
            self.updatehours(managers, openmanager)
            daily.remove(openmanager)
            closemanager = random.choice(daily)
            week[day]['1:30'].append(closemanager)
            self.updatehours(managers, closemanager)
            daily.remove(closemanager)
        for day in week.keys():
            if self.mavail[0] not in [i[0] for i in week[day].values() if i]:
                week[day]['11:00'].append(self.mavail[0])
                managers[self.mavail[0]] += 8
                break
                        
        
                