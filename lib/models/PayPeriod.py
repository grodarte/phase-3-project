from models.__init__ import CURSOR, CONN
from datetime import datetime


class PayPeriod:
    
    all = {}

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
        ''' Expects date in format: MM/DD/YY '''
        #uses date time to properly assign date
        try:
            date_obj = datetime.strptime(f'start_date', "%m/%d/%y")

            formatted_date = date_obj.strftime("%m-%d-%y")

            print(formatted_date)
        except ValueError:
            print("Invalid date format. Please enter the date as MM/DD/YY.")

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        ''' Expects date in format: MM/DD/YY '''
        # uses date time to properly assign date
        try:
            date_obj = datetime.strptime(f'end_date', "%m/%d/%y")

            formatted_date = date_obj.strftime("%m-%d-%y")

            print(formatted_date)
        except ValueError:
            print("Invalid date format. Please enter the date as MM/DD/YY.")

    @classmethod
    def create_table(cls):
        ''' Create a new table to persist the attributes of PayPeriod instances '''
        sql = '''
            CREATE TABLE IF NOT EXISTS payperiods (
            id INT PRIMARY KEY,
            start_date TEXT,
            end_date TEXT
            );
        '''

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        ''' Drop the table that persists PayPeriod instances '''
        sql = '''
            DROP TABLE IF EXISTS payperiods
        '''

        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        ''' Inserts a new row with the start and end date values of the current PayPeriod instance.
            Update object id attribute using the primary key value of the new row.
            Save the object in local dictionary using table row's PK as dictionary key '''
        sql = '''
            INSERT INTO payperiods(id, start_date, end_date)
            VALUES(?, ?, ?);
        '''

        CURSOR.execute(sql, (self.start_date, self.end_date))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, start_date, end_date):
        ''' initializes a new PayPeriod instance and saves the object to the database '''
        payperiod = cls(start_date, end_date)
        payperiod.save()
        return payperiod

    @classmethod
    def instance_from_db(cls, row):
        ''' Return a PayPeriod object having the attribute values from the table row '''
        
breakpoint()