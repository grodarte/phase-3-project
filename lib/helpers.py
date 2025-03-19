# lib/helpers.py
from models.shift import Shift
from models.payperiod import PayPeriod

def exit_program():
    print("Exiting program. Goodbye!")
    exit()

def get_payperiods():
    pass

def enumerate_payperiods(payperiods):
    pass

def create_payperiod():
    pass

def update_payperiod(payperiod_obj):
    pass

def calculate_payperiod_earnings(payperiod_obj):
    pass

def get_shifts(payperiod_obj):
    pass

def enumerate_shifts(shifts):
    pass

def display_shift_details(shift_obj):
    pass

def create_shift(payperiod_id):
    pass

def update_shift(shift_obj):
    pass

def delete_shift(shift_obj):
    pass


# def hours_worked(time_in, time_out):
#     """Calculate hours worked as a decimal number."""
#     h_in, m_in = map(int, self.clock_in.split(":"))
#     h_out, m_out = map(int, self.clock_out.split(":"))

#     total_minutes = (h_out * 60 + m_out) - (h_in * 60 + m_in)
#     if total_minutes < 0:
#         raise ValueError("Clock-out time must be after clock-in time")

#     return round(total_minutes / 60, 2)

# def total_tips(cc, cash):
#     return cc + cash

# #NEED TO UPDATE, piece by piece validation
# def create_shift():
#     print("Creating shift fn")
#     year = input("Enter the shift year as 'YY': ")
#     month = input("Enter the shift month: ")
#     day = input("Enter the shift day: ")
#     clock_in = input("Enter clock-in time as 'HH:MM AM/PM': ")
#     clock_out = input("Enter clock-out time as 'HH:MM AM/PM': ")
#     cc_tip = input("Enter tips earned via credit card: ")
#     cash_tip = input("Enter cash tips earned: ")
#     try:
#         shift = Shift.create(year, month, day, clock_in, clock_out, cc_tip, cash_tip)
#         print(f"Shift on {self.month}/{self.day}/{self.year} | In: {self.clock_in} | Out: {self.clock_out} | "
#                 f"Hours: {self.hours_worked(clock_in, clock_out)} | Tips: ${self.total_tips(cc_tip, cash_tip):.2f}")
#         # replace with repr f string
#     except Exception as exc:
#         print("Error creating shift: ", exc)
