from takeinput import Input
from algo3 import Week
from buildoutput import Spreadsheet
from cleanlist import xlfriendly
import os


def find_file(path):

    for file in os.listdir(path):
        if file.endswith('.xlsx'):
            return(folder + '/' + file)


def create_schedule(startdate):

    database = Input(orig_xl)
    roughschedule = Week()
    tbwsched = xlfriendly(roughschedule.schedule2, orig_xl)
    Spreadsheet(orig_xl, startdate, roughschedule.schedule2, folder)


folder = os.getcwd()
orig_xl = find_file(folder)

if __name__ == '__main__':

    create_schedule('8/14/16')