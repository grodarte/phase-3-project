# lib/helpers.py
from models.shift import Shift
from models.payperiod import PayPeriod

def exit_program():
    print("Exiting program. Goodbye!")
    exit()

def format_payperiod(payperiod):
    return f'{payperiod._smonth}/{payperiod._sday}/{payperiod._syear} - {payperiod._emonth}/{payperiod._eday}/{payperiod._eyear}'

def get_payperiods():
    payperiods = PayPeriod.get_all()
    return payperiods

def enumerate_payperiods(payperiods):
    print("\nPAY PERIODS:")
    print("**************************")
    for i, payperiod in enumerate(payperiods, start=1):
        print(f'{i}. {format_payperiod(payperiod)}')
    print("\n**************************")


def create_payperiod():
    print("\nPay period begins on:")
    smonth = input("Enter month (1-12): ")
    sday = input("Enter day (1-31): ")
    syear = input("Enter year (YYYY): ")
    print("\nPay period ends on:")
    emonth = input("Enter month (1-12): ")
    eday = input("Enter day (1-31): ")
    eyear = input("Enter year (YYYY): ")
    try:
        payperiod = PayPeriod.create(int(smonth), int(sday), int(syear), int(emonth), int(eday), int(eyear))
        print(f'\nSuccess: {format_payperiod(payperiod)}')
    except Exception as e:
        print("\nError creating pay period: ", e)

def update_payperiod(payperiod_obj):
    id_ = payperiod_obj.id
    try:
        print("Enter the updated pay period information or hit <enter> to leave it as is!")
        print("\nPay period begins on:")
        smonth = input(f"Current Month: {payperiod_obj._smonth} | New month (1-12): ")
        if smonth: payperiod_obj.smonth = int(smonth)
        sday = input(f"Current Day: {payperiod_obj._sday} | New day (1-31): ")
        if sday: payperiod_obj.sday = int(sday)
        syear = input(f"Current Year: {payperiod_obj._syear} | New year (YYYY): ")
        if syear: payperiod_obj.syear = int(syear)
        print("\nPay period ends on:")
        emonth = input(f"Current Month: {payperiod_obj._emonth} | New month (1-12): ")
        if emonth: payperiod_obj.emonth = int(emonth)
        eday = input(f"Current Day: {payperiod_obj._eday} | New day (1-31): ")
        if eday: payperiod_obj.eday = int(eday)
        eyear = input(f"Current Year: {payperiod_obj._eyear} | New year (YYYY): ")
        if eyear: payperiod_obj.eyear = int(eyear)

        payperiod_obj.update()
        print(f'\nSuccess: {format_payperiod(payperiod_obj)}')
    except Exception as e:
        print("Error updating department: ", e)

def calculate_payperiod_earnings(payperiod_obj):
    pass

def get_shifts(payperiod_obj):
    shifts = payperiod_obj.shifts()
    return shifts

def enumerate_shifts(selected_payperiod, shifts):
    print(f'\nShifts in Pay Period: {format_payperiod(selected_payperiod)}')
    print("**************************")
    if shifts:
        for i, shift in enumerate(shifts, start=1):
            print(f'{i}. {shift._month}/{shift._day}/{shift._year} | Hours: {hours_worked(shift._clock_in, shift._clock_out)} | Tips: {shift._cc_tip + shift._cash_tip}')
    else:
        print("\nNo shifts recorded.")
    print("\n**************************")    

def display_shift_details(shift_obj):
    print(f'\nSHIFT DETAILS ON: {shift_obj._month}/{shift_obj._day}/{shift_obj._year}')
    print("**************************")
    print(f'\nClock In Time: {shift_obj._clock_in}')
    print(f'Clock Out Time: {shift_obj._clock_out}')
    print(f'Hours Worked: {hours_worked(shift_obj._clock_in, shift_obj._clock_out)} hours')
    print(f'\nCredit Card Tips: ${shift_obj._cc_tip}')
    print(f'Cash Tips: ${shift_obj._cash_tip}')    
    print("\n**************************")


def create_shift(payperiod_id):
    pass

def update_shift(shift_obj):
    pass

def delete_shift(shift_obj):
    pass


def hours_worked(time_in, time_out):
    """Calculate hours worked as a decimal number."""
    h_in, m_in = map(int, time_in.split(":"))
    h_out, m_out = map(int, time_out.split(":"))

    total_minutes = (h_out * 60 + m_out) - (h_in * 60 + m_in)
    if total_minutes < 0:
        raise ValueError("Clock-out time must be after clock-in time")

    return round(total_minutes / 60, 2)