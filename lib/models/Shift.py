from models.__init__ import CURSOR, CONN
from models.payperiod import PayPeriod
from datetime import datetime, date
from decimal import Decimal

class Shift:

    all = {}

    def __init__(self, year, month, day, clock_in, clock_out, cc_tip, cash_tip):
        self.year = year
        self.month = month
        self.day = day
        self.clock_in = clock_in 
        self.clock_out = clock_out
        self.cc_tip = cc_tip
        self.cash_tip = cash_tip

    def __repr__(self):
        return f'Shift on {self.formatted_date()} | In: {self._clock_in} | Out: {self._clock_out}' or "Not set"
    

    # Year property
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        """Convert 2-digit year to 4-digit (assumes 2000-2049, 1950-1999)."""
        if year in range(0, 100):
            self._year = 2000 + year if year <= 49 else 1900 + year
        else:
            raise ValueError("Year must be in YY format, between 0 and 99.")

        if hasattr(self, '_month') and hasattr(self, '_day'):
            self._validate_day(self._year, self._month, self._day)

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

        if hasattr(self, '_year') and hasattr(self, '_day'):
            self._validate_day(self._year, self._month, self._day)
    
    # Day property
    @property
    def day(self):
        self._day
    
    @day.setter
    def day(self, day):
        self._validate_day(self._year, self._month, day)
        self._day = day

    # Date property
    @property
    def shift_date(self):
        """Return shift date as a 'datetime.date' object."""
        return date(self._year, self._month, self._day)

    @shift_date.setter
    def shift_date(self, new_date):
        """Set shift date using a tuple (year, month, day)."""
        self.year, self.month, self.day = new_date

    # Validate date using datetime
    def _validate_day(self, year, month, day):
        """Try to create a date with the given year, month, and day."""
        try:
            date(year, month, day)
        except ValueError as err:
            raise ValueError(f'Invalid date: {err}')

    # Format date MM/DD/YY
    def formatted_date(self):
        return self.shift_date.strftime("%m/%d/%y")


    # Clock-in property
    @property
    def clock_in(self):
        return self._clock_in

    @clock_in.setter
    def clock_in(self, clock_in):
        """Convert 'HH:MM AM/PM' to 24-hour 'HH:MM' format."""
        new_clock_in = datetime.strptime(clock_in, "%I:%M %p")
        if hasattr(self, '_clock_out') and self._clock_out is not None: 
            if new_clock_in >= datetime.strptime(self._clock_out, "%H:%M"):
                raise ValueError("Clock-in time must be before clock-out time")
        self._clock_in = new_clock_in.strftime("%H:%M")

    # Clock-out property
    @property
    def clock_out(self):
        return self._clock_out

    @clock_out.setter
    def clock_out(self, clock_out):
        """Convert 'HH:MM AM/PM' to 24-hour 'HH:MM' format."""
        new_clock_out = datetime.strptime(clock_out, "%I:%M %p")
        if hasattr(self, '_clock_in') and self._clock_in is not None:
            if new_clock_out <= datetime.strptime(self._clock_in, "%H:%M"):
                raise ValueError("Clock-out time must be later than clock-in time")
        self._clock_out = new_clock_out.strftime("%H:%M")

    # Tip property (credit card)
    @property
    def cc_tip(self):
        return self._cc_tip

    @cc_tip.setter
    def cc_tip(self, cc_tip):
        if isinstance(cc_tip, (int, float)) and cc_tip is not None:
            tip_value = Decimal(str(cc_tip))
            two_decimal_value = tip_value.quantize(Decimal("0.01"))
            if tip_value == two_decimal_value:
                self._cc_tip = float(two_decimal_value)
                
            else:
                raise ValueError("Credit card tip must have exactly two decimals.")
        else:
            raise ValueError("Credit card tip must be a number with two decimal places.")

    # Tip property (cash)
    @property
    def cash_tip(self):
        return self._cash_tip

    @cash_tip.setter
    def cash_tip(self, cash_tip):
        if isinstance(cash_tip, (int, float)):
            tip_value = Decimal(str(cash_tip))
            two_decimal_value = tip_value.quantize(Decimal("0.01"))
            if tip_value == two_decimal_value:
                self._cash_tip = float(two_decimal_value)
            else:
                raise ValueError("Cash tip cannot have more than two decimal places.")
        else:
            raise ValueError("Credit card tip must be a number with no more than two decimal places.")

    # Pay period id property
    @property
    def payperiod_id(self):
        return self._payperiod_id

    @payperiod_id.setter
    def payperiod_id(self, payperiod_id):
        # if isinstance(payperiod_id, int) and PayPeriod.find_by_id(payperiod_id):
        #     self._payperiod_id = payperiod_id
        # else:
        #     raise ValueError("payperiod_id must reference a pay period in the database")
        pass

    # CREATE TABLE - cls
    @classmethod
    def create_table(cls):
        """ create a new table to persist the attributes of Shift instances """
        sql = """
            CREATE TABLE IF NOT EXISTS shifts;
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
            SET year = ?, month = ?, day = ?, clock_in = ?, clock_out = ?, cc_tip = ?, cash_tip = ?
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.year, self.month, self.day, self.clock_in, self.clock_out, self.cc_tip, self.cash_tip, self.id))
        CONN.commit()

    # DELETE
    def delete(self):
        """ delete the table tow corresponding to the current Shift instance,
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
        else:
        # create new instance and add to dictionary if doesnt already exist
            shift = cls(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
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
        """ returns shift object corresponding to the tabke row that matches the specified primary key """
        sql = """
            SELECT id from shifts
            WHERE id = ?;
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # FIND BY DATE RANGE - cls