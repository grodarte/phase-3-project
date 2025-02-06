from models.__init__ import CURSOR, CONN
from datetime import datetime


class PayPeriod:
    
    all = {}

    def __init__(self, smonth, sday, syear):
        self.smonth = smonth
        self.sday = sday
        self.syear = syear

    # Start month of pay period property
    @property
    def smonth(self):
        return self._smonth

    @smonth.setter
    def smonth(self, smonth):
        if isinstance(smonth, int) and smonth in range(1,13)

    # Start day of pay period property

    # Start year of pay period property

    # End month of pay period property

    # End day of pay period property

    # End year of pay period property

    # date validation method


    
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