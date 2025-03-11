from models.__init__ import CURSOR, CONN
from models.payperiod import PayPeriod
from datetime import datetime, date
from decimal import Decimal

class Shift:

    all = {}

    def __init__(self, year, month, day, clock_in, clock_out, cc_tip, cash_tip, payperiod, id=None):
        self.id = id
        self.year = year
        self.month = month
        self.day = day
        self.clock_in = clock_in 
        self.clock_out = clock_out
        self.cc_tip = cc_tip
        self.cash_tip = cash_tip
        self.payperiod_id = payperiod.id
    
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

    def validate_time(self, time_str):
    """Ensure time is in HH:MM format and valid."""
    try:
        hours, minutes = map(int, time_str.split(":"))
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return time_str
        except ValueError:
            pass
        raise ValueError("Time must be in HH:MM 24-hour format.")

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

    def _validate_tip(self, tip):
    """Validate tip amount to ensure it's a positive float with two decimals."""
    try:
        tip = round(float(tip), 2)
        if tip < 0:
            raise ValueError("Tip cannot be negative")
        return tip
    except ValueError:
        raise ValueError("Tip must be a positive number with up to two decimals")

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
            year INTEGER, 
            month INTEGER, 
            day INTEGER, 
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
            INSERT INTO shifts(year, month, day, clock_in, clock_out, cc_tip, cash_tip)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        CURSOR.execute(sql, (self.year, self.month, self.day, self.clock_in, self.clock_out, self.cc_tip, self.cash_tip))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    # CREATE - cls
    @classmethod
    def create(cls, year, month, day, clock_in, clock_out, cc_tip, cash_tip):
        """ initialize a new Shift instance and save the object to the database
            return new Shift object """
        shift = cls(year, month, day, clock_in, clock_out, cc_tip, cash_tip)
        shift.save()

    # UPDATE
    def update(self):
        """ updates the corresponding table row for the current Shift instance """
        sql = """
            UPDATE shifts
            SET year = ?, month = ?, day = ?, clock_in = ?, clock_out = ?, cc_tip = ?, cash_tip = ?, payperiod_id = ?
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.year, self.month, self.day, self.clock_in, self.clock_out, self.cc_tip, self.cash_tip, self.payperiod_id, self.id))
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
        shift = cls.all.get(row(0))
        if shift:
        # ensure attributes match row values in case local instance was modified
            shift.year = row[1]
            shift.month = row[2]
            shift.day = row[3]
            shift.clock_in = row[4]
            shift.clock_out = row[5]
            shift.cc_tip = row[6]
            shift.cash_tip = row[7]
            shift.payperiod_id = row[8]
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


    # moving to front end logic
    """ simplify below functions in front end logic to calculate as needed for selected shift """

    # # Hours worked method to shift
    # def hours_worked(self):
    #     """ returns total hours worked for current shift instance """
    #     in_time = datetime.strptime(self.clock_in, "%H:%M")
    #     out_time = datetime.strptime(self.clock_out, "%H:%M")
    #     return (out_time - in_time).total_seconds() / 3600

    # def wages_earned(self, wage=16.5, overtime_rate=1.5):
    #     """ returns wages earned for current shift instance based on hourly at minimum wage if wage not provided,
    #         calculates for overtime being time and a half (1.5x) if not provided"""
    #     total_wages = 0
    #     if wage <= 8:
    #         total_wages = self.hours_worked() * wage
    #     else:
    #         overtime_hours = self.hours_worked() - 8
    #         total_wages = (8 * wage) + (overtime_hours * (wage * overtime_rate))
    #     return total_wages        

    # # total earned - hourly and tips
    # def total_earned(self):
    #     """ returns total earned for current shift instance including wages and tips """
    #     tips = self.cc_tips + self.cash_tips
    #     wages = self.wages_earned()
    #     return tips + wages