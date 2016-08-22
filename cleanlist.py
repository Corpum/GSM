from algo3 import Week
from openpyxl import load_workbook
from translate import trans

# Load in Week()
zap = Week()
# Assign schedule
zap = zap.schedule2


# Replaces days of the week with their coordinates
for name in zap:
    for shift in zap[name]:
        if shift[0] in trans.keys():
            shift[0] = trans[shift[0]]

# Load in Our Excel document
wb = load_workbook('Goodwill_schedule.xlsx')
sh = wb.get_sheet_by_name('Sheet1')
# Find the name in the Excel Document, replace it with Row value
for i in range(1, 42):
    if sh.cell(row=i, column=1).value in zap.keys():
        zap[i] = zap[sh.cell(row=i, column=1).value]
        del zap[sh.cell(row=i, column=1).value]
