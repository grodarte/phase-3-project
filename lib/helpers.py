# lib/helpers.py
from models.shift import Shift
from models.payperiod import PayPeriod

def view_all_payperiods():
    pass

def view_shifts_in_payperiod():
    pass

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
