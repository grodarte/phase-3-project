from models.__init__ import CURSOR, CONN
from datetime import date


class PayPeriod:
    
    all = []

    def __init__(self, start_month, start_day, start_year, end_month, end_day, end_year, id=None):
        self.id = id
        self._start_date = None
        self._end_date = None
        self.set_start_date(start_month, start_day, start_year)
        self.set_end_date(end_month, end_day, end_year)

    def __repr__(self):
        return f'Pay Period {self.id}: {self.start_date} - {self.end_date}'
    
    @property
    def start_date(self):
        return self._start_date

    def set_start_date(self, month, day, year):
        try:
            new_start_date = date(year, month, day)
            if self._end_date and new_start_date > self._end_date:
                raise ValueError("Start date cannot be after the end date.")
            self._start_date = new_start_date
        except ValueError as e:
            print(f'Invalid start date: {e}')

    @property
    def end_date(self):
        return self._end_date

    def set_end_date(self, month, day, year):
        try:
            new_end_date = date(year, month, day)
            if self._start_date and new_end_date < self._start_date:
                raise ValueError("End date cannot be before the start date.")
            self._end_date = new_end_date
        except ValueError as e:
            print(f'Invalid end date: {e}')

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of the PayPeriod instances """
        sql = """
            CREATE TABLE IF NOT EXISTS payperiods (
            id INTEGER PRIMARY KEY,
            start_date TEXT,
            end_date TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

breakpoint()