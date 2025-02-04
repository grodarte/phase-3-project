from models.__init__ import CURSOR, CONN
from models.payperiod import PayPeriod
from datetime import datetime

class Shift:
    def __init__(self, date, clock_in, clock_out, cc_tips, cash_tips, payperiod_id=None, id=None):
        self.id = id
        self.date = date
        self.clock_in = clock_in
        self.clock_out = clock_out
        self.cc_tips = cc_tips
        self.cash_tips = cash_tips
        self.payperiod_id = payperiod_id

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        ''' expects date in format: D/M/YYYY '''
        # use date time to assign proper date
        pass

    @property
    def clock_in(self):
        return self._clock_in

    @clock_in.setter
    def clock_in(self, clock_in):
        # use date time to assign proper time
        pass

    @property
    def clock_out(self):
        return self._clock_in

    @clock_out.setter
    def clock_out(self, clock_out):
        # use date time to assign proper time
        pass

    @property
    def cc_tips(self):
        return self.cc_tips

    @cc_tips.setter
    def cc_tips(self, cc_tips):
        # assigns tip value for cc
        pass

    @property
    def cash_tips(self):
        return self._cash_tips

    @cash_tips.setter
    def cash_tips(self, cash_tips):
        # assigns cash tip value
        pass

    @property
    def payperiod_id(self):
        return self._payperiod_id

    @payperiod_id.setter
    def payperiod_id(self, payperiod_id):
        #checks PayPeriods to see if a pay period exists for the date
        #if it does - assigns pay period id accordingly
        # if it doesnt - calls fn to create a payperiod which will then be assigned to it
        pass