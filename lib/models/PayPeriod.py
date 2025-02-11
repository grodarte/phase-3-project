from models.__init__ import CURSOR, CONN
from datetime import datetime, date


class PayPeriod:
    
    all = {}

    def __init__(self, syear, smonth, sday, eyear, emonth, eday):
        self.syear = syear
        self.smonth = smonth
        self.sday = sday
        self.eyear = eyear
        self.emonth = emonth
        self.eday = eday

    def __repr__(self):
        return f'Pay period: {self._smonth}/{self._sday}/{self._syear} - End Date'

    # Start year of pay period property
    @property
    def syear(self):
        return self._syear

    @syear.setter
    def syear(self, syear):
        """Convert 2 digit year to 4 digit year"""
        self._syear = 2000 + syear if syear <= 49 else 1900 + syear

        if (hasattr(self, '_smonth') and hasattr(self, '_sday')):
            self._validate_date(self._syear, self._smonth, self._sday)

    # Start month of pay period property
    @property
    def smonth(self):
        return self._smonth

    @smonth.setter
    def smonth(self, smonth):
        if smonth in range(1,13):
            self._smonth = smonth
        else:
            raise ValueError("Month must be between 1 and 12.")

        if hasattr(self, '_syear') and hasattr(self, '_sday'):
            self._validate_day(self._syear, self._smonth, self._sday)

    # Start day of pay period property
    # @property
    # def sday(self):
    #     return self._sday

    # @sday.setter
    # def sday(self, sday):
    #     self._validate_date(self._syear, self._smonth, sday)
    #     self._sday = sday

    # # End year of pay period property
    # @property
    # def eyear(self):
    #     return self._eyear

    # @eyear.setter
    # def eyear(self, eyear):
    #     if eyear in range(0, 100):


    # End month of pay period property

    # End day of pay period property


    # date validation method
    def _validate_date(self, year, month, day):
        """Try to create a date with the given year, month and day"""
        try:
            date(year, month, day)
        except ValueError as err:
            raise ValueError(f'Invalid date: {err}')

    
    # CREATE TABLE - cls

    # DROP TABLE - cls

    # SAVE

    # CREATE - cls

    # UPDATE

    # DELETE

    # INSTANCE FROM DB - cls

    # GET ALL - cls

    # FIND BY ID - cls

    # shifts