from models.__init__ import CURSOR, CONN
from datetime import datetime, date


class PayPeriod:
    
    all = {}

    def __init__(self, syear, smonth, sday, eyear, emonth, eday, id=None):
        self.id = id
        self.syear = syear
        self.smonth = smonth
        self.sday = sday
        self.eyear = eyear
        self.emonth = emonth
        self.eday = eday

    def __repr__(self):
        return f'Pay period: {self._smonth}/{self._sday}/{self._syear} - {self._emonth}/{self._eday}/{self._eyear}'

    # Start year property
    @property
    def syear(self):
        return self._syear

    @syear.setter
    def syear(self, syear):
        if syear in range(2000, 2026):
            self._syear = syear
        else:
            raise ValueError("Year must be in YYYY format, between 2000 and 2026.")

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

    # Start day property
    @property
    def sday(self):
        return self._sday

    @sday.setter
    def sday(self, sday):
        if sday in range(1,32):
            self._sday = sday
        else: 
            raise ValueError("Day must be between 1 and 31.")

    # End year property
    @property
    def eyear(self):
        return self._eyear

    @eyear.setter
    def eyear(self, eyear):
        if eyear in range(2000, 2026):
            self._eyear = eyear
        else:
            raise ValueError("Year must be in YYYY format, between 2000 and 2026.")

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

    # End day property
    @property
    def eday(self):
        return self._eday

    @eday.setter
    def eday(self, eday):
        if eday in range(1,32):
            self._eday = eday
        else:
            raise ValueError("Day must be between 1 and 31.")
    
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
            return payperiod
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