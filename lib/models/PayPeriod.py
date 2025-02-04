from models.__init__ import CURSOR, CONN
from datetime import date


class PayPeriod:
    
    all = []

    def __init__(self, start_date, end_date, id=None):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f'Pay Period {self.id}: {self.start_date} - {self.end_date}'
    
    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        ''' Expects date in format: D/M/YYYY '''
        #uses date time to properly assign date
        pass

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        ''' Expects date in format: D/M/YYYY '''
        # uses date time to properly assign date
        pass


        
breakpoint()