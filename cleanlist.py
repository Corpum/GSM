from algo3 import Week
import numpy as np
from openpyxl import Workbook
from openpyxl import load_workbook

# Load in Week()
zap = Week()
# Assign schedule
zap = zap.schedule2

# The structure we will use to translate weekdays into Excel Coordinates
trans = {'sunday':4,
         'monday':7,
         'tuesday':10,
         'wednesday':13,
         'thursday':16,
         'friday':19,
         'saturday':22
         }

# Replaces days of the week with their coordinates
for name in zap:
    for shift in zap[name]:
        if shift[0] in trans.keys():
            shift[0] = trans[shift[0]]

# Load in Our Excel document
wb = load_workbook('Goodwill_schedule.xlsx')
sh = wb.get_sheet_by_name('Sheet1')
# Find the name in the Excel Document, replace it with Row value
for i in range(1,42):
    if sh.cell(row=i, column=1).value in zap.keys():
        zap[i] = zap[sh.cell(row=i, column=1).value]
        del zap[sh.cell(row=i, column=1).value]
        
    