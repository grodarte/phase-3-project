from models.__init__ import CURSOR, CONN
from models.payperiod import PayPeriod
import datetime

class Shift:

    all = {}

    def __init__(self, month, day, year):
        self._workday = None
        self.workday = (month, day, year)

    @property
    def workday(self):
        return self._workday

    @workday.setter
    def workday(self, date_tuple):
        ''' sets workday using datetime and passing in month, day and year as a tuple '''
        month, day, year = date_tuple
        try:
            shift_date = datetime.date(year, month, day)
            self._workday = shift_date

        except ValueError:
            print("Invalid date format. Please enter the date as MM/DD/YY.")