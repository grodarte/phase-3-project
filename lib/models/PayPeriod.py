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
        return f'Pay period: {self._smonth}/{self._sday}/{self._syear} - {self._emonth}/{self._eday}/{self._eyear}'

    def _validate_period(self):
        """Ensure that the start date is before or equal to the end date."""

    # Date validation method
    def _validate_date(self, year, month, day):
        """Try to create a date with the given year, month and day"""
        try:
            date(year, month, day)
        except ValueError as err:
            raise ValueError(f'Invalid date: {err}')

        # Validates that start date is before or equal to the end date
        if (hasattr(self, '_syear') and hasattr(self, '_smonth') and hasattr(self, '_sday') and hasattr(self, '_eyear') and hasattr(self, '_emonth') and hasattr(self, '_eday')):
            start = date(self._syear, self._smonth, self._sday)
            end = date(self._eyear, self._emonth, self._eday)
            if start > end:
                raise ValueError("Start date must be before or equal to the end date.")

    # Start year property
    @property
    def syear(self):
        return self._syear

    @syear.setter
    def syear(self, syear):
        """Convert 2 digit year to 4 digit year"""
        if syear in range(0, 100):
            self._syear = 2000 + syear if syear <= 49 else 1900 + syear
        else:
            raise ValueError("Year must be in YY format, between 0 and 99.")

        if (hasattr(self, '_smonth') and hasattr(self, '_sday')):
            self._validate_date(self._syear, self._smonth, self._sday)

    # Start month property
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
            self._validate_date(self._syear, self._smonth, self._sday)

    # Start day property
    @property
    def sday(self):
        return self._sday

    @sday.setter
    def sday(self, sday):
        self._validate_date(self._syear, self._smonth, sday)
        self._sday = sday

    # End year property
    @property
    def eyear(self):
        return self._eyear

    @eyear.setter
    def eyear(self, eyear):
        if eyear in range(0, 100):
            self._eyear = 2000 + eyear if eyear <= 49 else 1900 + eyear
        else:
            raise ValueError("Year must be in YY format, between 0 and 99.")
        
        if (hasattr(self, '_emonth') and hasattr(self, '_eday')):
            self._validate_date(self._eyear, self._emonth, self._eday)

    # End month property
    @property
    def emonth(self):
        return self._emonth

    @emonth.setter
    def emonth(self, emonth):
        if 1 <= emonth <= 12:
            self._emonth = emonth
        else:
            raise ValueError("Month must be between 1 and 12.")
    
        if (hasattr(self, '_eyear') and hasattr(self, '_eday')):
            self._validate_date(self._eyear, self._emonth, self._eday)

    # End day property
    @property
    def eday(self):
        return self._eday

    @eday.setter
    def eday(self, eday):
        self._validate_date(self._eyear, self._emonth, eday)
        self._eday = eday
    
    # CREATE TABLE - cls
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of PayPeriod instances """
        sql = """
            CREATE TABLE IF NOT EXISTS payperiods (
            id INTEGER PRIMARY KEY,
            smonth INTEGER,
            sday INTEGER,
            syear INTEGER,
            emonth INTEGER,
            eday INTEGER,
            eyear INTEGER
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    # DROP TABLE - cls
    @classmethod
    def drop_table(cls):
        """ Drop the table that persists PayPeriod instances """
        sql = """
            DROP TABLE IF EXISTS payperiods;
        """
        CURSOR.execute(sql)
        CONN.commit()

    # SAVE
    def save(self):
        """ Insert a new row with the start and end date values (month, day, year) of the current PayPeriod
        Update payperiod id attribute using the primary key value of each row.
        Save the object in local dictionary using the table row's PK as dictionary key"""
        sql = """
            INSERT INTO payperiods(smonth, sday, syear, emonth, eday, eyear)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        CURSOR.execute(sql, (self.smonth, self.sday, self.syear, self.emonth, self.eday, self.eyear))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    # CREATE - cls
    @classmethod
    def create(cls, syear, smonth, sday, eyear, emonth, eday):
        """ Initialize a new PayPeriod instance and save the object to the database"""
        payperiod = cls(syear, smonth, sday, eyear, emonth, eday)
        payperiod.save()
        return payperiod

    # UPDATE
    def update(self):
        """ Update the table row corresponding to the current PayPeriod instance """
        sql = """
            UPDATE payperiods
            SET smonth = ?, sday = ?, syear = ?, emonth = ?, eday = ?, eyear = ?
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.smonth, self.sday, self.syear, self.emonth, self.eday, self.eyear, self.id))
        CONN.commit()

    # DELETE
    def delete(self):
        """ Delete the table row corresponding to the current PayPeriod instance,
        delete the dictionary entry, and reassign the id attribute """
        sql = """
            DELETE FROM payperiods
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    # INSTANCE FROM DB - cls
    @classmethod
    def instance_from_db(cls, row):
        """ Return a payperiod object having the attribute values from the table row """
        #check the dictionary for an existing instance using the row's primary key row[0]
        payperiod = cls.all.get(row[0])
        if payperiod:
            #ensure attributes match row values in case local instance was modified
            payperiod.smonth = row[1]
            payperiod.sday = row[2]
            payperiod.syear = row[3]
            payperiod.emonth = row[4]
            payperiod.eday = row[5]
            payperiod.eyear = row[6]
        else:
            #create new instance and add to dictionary
            payperiod = cls(row[1], row[2], row[3], row[4], row[5], row[6])
            payperiod.id = row[0]
            cls.all[payperiod.id] = payperiod
        return payperiod

    # GET ALL - cls
    @classmethod
    def get_all(cls):
        """ Return a list containing a payperiod object per row in the table """
        # SHOULD I ADD ON ASCENDING OR DESCENDING ORDER?
        sql = """
            SELECT * FROM payperiods;
        """
        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    # FIND BY ID - cls
    @classmethod
    def find_by_id(cls, id):
        """ Return a payperiod object corresponding to the table row matching the specified primary key """
        sql = """
            SELECT id FROM payperiods
            WHERE id = ?;
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # FIND BY DATE - cls
    @classmethod
    def find_by_date(cls, year, month, day):
        """ Return a payperiod object corresponding to the table row containing the specified date """
        sql = """
            SELECT * FROM payperiods
            WHERE (syear || '-' || smonth || '-' || sday) <= (? || '-' || ? || '-' || ?) 
            AND (eyear || '-' || emonth || '-' || eday) >= (? || '-' || ? || '-' || ?);
        """
        row = CURSOR.execute(sql, (year, month, day, year, month, day)).fetchone()
        return cls.instance_from_db(row) if row else None

    def shifts(self):
        """ Return list of shifts associated with the current payperiod """
        from models.shift import Shift
        sql = """
            SELECT * FROM shifts
            WHERE payperiod_id = ?;
        """
        CURSOR.execute(sql, (self.id,))
        row = CURSOR.fetchall()
        return [Shift.instance_from_db(row) for row in rows]

    # total tips per pay period

    # total hourly per pay period

    # average hourly including tips