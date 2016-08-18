from cleanlist import zap
from openpyxl import Workbook
from openpyxl import load_workbook

print(zap)
class Spreadsheet():
    
    def __init__(self):
        self.createdoc()
        self.writetodoc()
        
    def createdoc(self):
        self.wb = load_workbook('Goodwill_schedule.xlsx')
        self.sh = self.wb.get_sheet_by_name('Sheet1')
        
    def writetodoc(self):
        '''Writes information from Week() to Excel sheet'''
        for r in zap:
            for col,time in zap[r]:
                self.sh.cell(row=r, column = col).value = str(time)
        self.wb.save('updated_sched3.xlsx')
                
                
                
        
                