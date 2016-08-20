from openpyxl import load_workbook
from cleanlist import trans
import sqlite3 as lite


class Input():

    def __init__(self):
        self.trans2 = {v: k for k, v in trans.items()}
        self.info = {}
        self.id = 1
        self.position = 1
        self.load_doc()
        self.build_dict()

    def load_doc(self):
        self.wb = load_workbook('template_schedule.xlsx')
        self.sh = self.wb.get_sheet_by_name('Sheet1')

    def build_dict(self):
        '''Search the lefthand column for names'''
        for r in range(1, 50):
            entry = str(self.sh.cell(row=r, column=1).value)
            if entry.isupper():
                # Find values for ID, position,
                self.info[entry] = [self.id, entry, self.position]
                self.id += 1
                _type = self.sh.cell(row=r, column=6).value
                if _type == 'F':
                    self.info[entry].append(1)
                elif _type == 'B':
                    self.info[entry].append(2)
                else:
                    self.info[entry].append(3)
                for c in [4, 7, 10, 13, 16, 19, 22]:
                    availability = str(self.sh.cell(row=r, column=c).value)
                    if availability == 'X':
                        self.info[entry].append(self.trans2[c])
            elif entry == 'Management':
                self.position = 1

            elif entry == 'Full Time Store Associates':
                self.position = 2

            elif entry == 'Part Time Associates':
                self.position = 3

            else:
                continue

    def init_db(self):

        self.db = lite.connect('employees3.db')
        self.cur = self.db.cursor()

    def build_db(self):

        self.cur.execute('CREATE TABLE employees ('
                         + 'id INTEGER NOT NULL PRIMARY KEY,'
                         + 'name VARCHAR(25) UNIQUE,'
                         + 'type INTEGER NOT NULL,'
                         + 'hours FLOAT NOT NULL DEFAULT 0,'
                         + 'maxhours FLOAT NOT NULL DEFAULT 1,'
                         + 'sunday INTEGER NOT NULL DEFAULT 1,'
                         + 'monday INTEGER NOT NULL DEFAULT 1,'
                         + 'tuesday INTEGER NOT NULL DEFAULT 1,'
                         + 'wednesday INTEGER NOT NULL DEFAULT 1,'
                         + 'thursday INTEGER NOT NULL DEFAULT 1,'
                         + 'friday INTEGER NOT NULL DEFAULT 1,'
                         + 'satuday INTEGER NOT NULL DEFAULT 1)')

    def insert(self):

        pass

if __name__ == '__main__':

    i = Input()
