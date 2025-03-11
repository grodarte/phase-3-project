# lib/helpers.py
from models.shift import Shift
from models.payperiod import PayPeriod

def view_all_payperiods():
    pass

def view_shifts_in_payperiod():
    pass



def hours_worked(time_in, time_out):
    """Calculate hours worked as a decimal number."""
    h_in, m_in = map(int, self.clock_in.split(":"))
    h_out, m_out = map(int, self.clock_out.split(":"))

    total_minutes = (h_out * 60 + m_out) - (h_in * 60 + m_in)
    if total_minutes < 0:
        raise ValueError("Clock-out time must be after clock-in time")

    return round(total_minutes / 60, 2)


def create_shift():
    print("Creating shift fn")
    year = input("Enter the shift year as 'YY': ")
    month = input("Enter the shift month: ")
    day = input("Enter the shift day: ")
    clock_in = input("Enter clock-in time as 'HH:MM AM/PM': ")
    clock_out = input("Enter clock-out time as 'HH:MM AM/PM': ")
    cc_tip = input("Enter tips earned via credit card: ")
    cash_tip = input("Enter cash tips earned: ")
    try:
        shift = Shift.create(year, month, day, clock_in, clock_out, cc_tip, cash_tip)
        print(f'Shift on {self.formatted_date()} | In: {self._clock_in} | Out: {self._clock_out} | Tips: {self.cc_tip + self.cash_tip}')
        # replace with repr f string
    except Exception as exc:
        print("Error creating shift: ", exc)

def view_shift():
    pass

def edit_shift():
    pass

def delete_shift():
    pass

def exit_program():
    print("Exiting program. Goodbye!")
    exit()
