from models.__init__ import CURSOR, CONN
from models.payperiod import PayPeriod

class Shift:

    all = {}

    def __init__(self, month, day, year, clock_in, clock_out, cc_tip, cash_tip, payperiod_id, id=None):
        self.id = id
        self.month = month
        self.day = day
        self.year = year
        self.clock_in = clock_in 
        self.clock_out = clock_out
        self.cc_tip = cc_tip
        self.cash_tip = cash_tip
        self.payperiod_id = payperiod_id
    
    # Year property
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        if year in range(2000, 2026):
            self._year = year
        else:
            raise ValueError("Year must be in YYYY format, between 2000 and 2025.")

    # Month property
    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, month):
        if (1 <= month <= 12):
            self._month = month
        else:
            raise ValueError("Month must be between 1 and 12.")
    
    # Day property
    @property
    def day(self):
        return self._day
    
    @day.setter
    def day(self, day):
        if (0 < day < 32):
            self._day = day
        else:     
            raise ValueError("Day must be between 1 and 31.")


    # Clock-in property
    @property
    def clock_in(self):
        return self._clock_in

    @clock_in.setter
    def clock_in(self, clock_in):
        self._clock_in = self._validate_time(clock_in)

    # Clock-out property
    @property
    def clock_out(self):
        return self._clock_out

    @clock_out.setter
    def clock_out(self, clock_out):
        self._clock_out = self._validate_time(clock_out) 

    # validate time strings, minimize setter logic / redundancy
    def _validate_time(self, time_str):
        """Ensure time is in HH:MM format and valid."""
        try:
            hours, minutes = map(int, time_str.split(":"))
            if 0 <= hours < 24 and 0 <= minutes < 60:
                return time_str
        except ValueError:
            pass
        raise ValueError("Time must be in HH:MM 24-hour format.")


    # Tip property (credit card)
    @property
    def cc_tip(self):
        return self._cc_tip

    @cc_tip.setter
    def cc_tip(self, cc_tip):
        self._cc_tip = self._validate_tip(cc_tip)

    # Tip property (cash)
    @property
    def cash_tip(self):
        return self._cash_tip

    @cash_tip.setter
    def cash_tip(self, cash_tip):
        self._cash_tip = self._validate_tip(cash_tip)

    # validate tip integers, minimize setter logic / redundancy
    def _validate_tip(self, tip):
        """Validate tip amount to ensure it's a 0 or positive float with two decimals."""
        try:
            tip = round(float(tip), 2)
            if tip < 0:
                raise ValueError("Tip cannot be negative")
            return tip
        except ValueError:
            raise ValueError("Tip must be a 0 or positive number with up to two decimals")

    # PayPeriod object
    @property
    def payperiod_id(self):
        return self._payperiod_id

    @payperiod_id.setter
    def payperiod_id(self, payperiod_id):
        if type(payperiod_id) is int and PayPeriod.find_by_id(payperiod_id):
            self._payperiod_id = payperiod_id
        else:
            raise ValueError("payperiod_id must reference a pay period in the database.")

    # CREATE TABLE - cls
    @classmethod
    def create_table(cls):
        """ create a new table to persist the attributes of Shift instances """
        sql = """
            CREATE TABLE IF NOT EXISTS shifts(
            id INTEGER PRIMARY KEY,
            month INTEGER, 
            day INTEGER, 
            year INTEGER, 
            clock_in TEXT, 
            clock_out TEXT, 
            cc_tip FLOAT, 
            cash_tip INTEGER,
            payperiod_id INTEGER,
            FOREIGN KEY (payperiod_id) REFERENCES payperiod(id)
            );
        """
        CURSOR.execute(sql)
        CONN.commit()


    # DROP TABLE - cls
    @classmethod
    def drop_table(cls):
        """ drop table that persists the Shift instances """
        sql = """
            DROP TABLE IF EXISTS shifts;
        """
        CURSOR.execute(sql)
        CONN.commit()

    # SAVE
    def save(self):
        """ inserts a new row into the database to persist the attributes of Shift instance,
        updates shift id attribute using the primary key of each row,
        saves the object in the local dictionary using the primary key as the dictionary key """
        sql = """
            INSERT INTO shifts(month, day, year, clock_in, clock_out, cc_tip, cash_tip, payperiod_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        CURSOR.execute(sql, (self.month, self.day, self.year, self.clock_in, self.clock_out, self.cc_tip, self.cash_tip, self.payperiod_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    # CREATE - cls
    @classmethod
    def create(cls, month, day, year, clock_in, clock_out, cc_tip, cash_tip, payperiod_id):
        """ initialize a new Shift instance and save the object to the database
            return new Shift object """
        shift = cls(month, day, year, clock_in, clock_out, cc_tip, cash_tip, payperiod_id)
        shift.save()

        return shift

    # UPDATE
    def update(self):
        """ updates the corresponding table row for the current Shift instance """
        sql = """
            UPDATE shifts
            SET month = ?, day = ?, year = ?, clock_in = ?, clock_out = ?, cc_tip = ?, cash_tip = ?, payperiod_id = ?
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.month, self.day, self.year, self.clock_in, self.clock_out, self.cc_tip, self.cash_tip, self.payperiod_id, self.id))
        CONN.commit()

    # DELETE
    def delete(self):
        """ delete the table row corresponding to the current Shift instance,
        delete the dictionary entry, reassign the id attribute """
        sql = """
            DELETE FROM shifts
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    # INSTANCE FROM DB - cls
    @classmethod
    def instance_from_db(cls, row):
        """ return a payperiod object having the attribute values from the table row """
        # check the dictionary for an existing instance matching the row primary key
        shift = cls.all.get(row[0])
        if shift:
            return shift
        else:
        # create new instance and add to dictionary if doesnt already exist
            shift = cls(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            shift.id = row[0]
            cls.all[shift.id] = shift
            return shift


    # GET ALL - cls
    @classmethod
    def get_all(cls):
        """ return a list containing a shift object per row in the table """
        sql = """
            SELECT * FROM shifts;
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    # FIND BY ID - cls
    @classmethod
    def find_by_id(cls, id):
        """ returns shift object corresponding to the table row that matches the specified primary key """
        sql = """
            SELECT id FROM shifts
            WHERE id = ?;
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None