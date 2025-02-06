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
        return f'Shift on {self.formatted_date()} | In: {self.clock_in} | Out: {self.clock_out}' or "Not set"

    # Year property
    @property
    def year(self):
        return self._year

    #ADD VALIDATION
    @year.setter
    def year(self, value):
        """Convert 2-digit year to 4-digit (assumes 2000-2049, 1950-1999)."""
        self._year = 2000 + value if value <= 49 else 1900 + value

    # Month property - calls the shift date setter within

    # Day property - calls the shift date setter within

    # Date property
    @property
    def shift_date(self):
        """Return shift date as a 'datetime.date' object."""
        return date(self._year, self.month, self.day)

    #ADD VALIDATION
    @shift_date.setter
    def shift_date(self, new_date):
        """Set shift date using a tuple (year, month, day)."""
        self.year, self.month, self.day = new_date

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

    # DROP TABLE - cls

    # SAVE

    # CREATE - cls

    # UPDATE

    # DELETE

    # INSTANCE FROM DB - cls

    # GET ALL - cls

    # FIND BY ID - cls

    # FIND BY DATE RANGE - cls