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
    print("***************************")
    if payperiods:
        for i, payperiod in enumerate(payperiods, start=1):
            print(f'{i}. {format_payperiod(payperiod)}')
    else:
        print("\nNo pay periods recorded.")
    print("\n***************************")


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
    try:
        print("\nEnter the updated pay period information or hit <enter> to leave it as is!")
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

def delete_payperiod(selected_payperiod):
    try:
        shifts = get_shifts(selected_payperiod)
        for shift in shifts:
            shift.delete()
        print(f'\n{len(shifts)} shift(s) deleted successfully')
    except Exception as e:
        print("\nError deleting shifts: ", e)
    try:
        selected_payperiod.delete()
        print(f'Payperiod deleted successfully: {format_payperiod(selected_payperiod)}')
    except Exception as e:
        print("\nError deleting pay period: ", e)


def calculate_payperiod_earnings(payperiod_obj):
    regular_hours = 0
    overtime_hours = 0
    total_hours = regular_hours + overtime_hours
    cc_tips = 0
    cash_tips = 0
    total_tips = cc_tips + cash_tips
    wage = 16.50
    overtime_rate = 1.5
    overtime_wage = wage * overtime_rate

    try:
        print(f"\nEnter your wage or hit <enter> to proceed with earnings calculations at minimum wage (${wage})")
        wage_input = input("\n>>> ")
        if wage_input: wage = float(wage_input)

        for shift in get_shifts(payperiod_obj):
            cc_tips += shift.cc_tip
            cash_tips += shift.cash_tip
            total_hours_worked = hours_worked(shift)
            if total_hours_worked <= 8:
                regular_hours += total_hours_worked
            else:
                regular_hours += 8
                overtime_hours += (total_hours_worked - 8)
    except Exception as e:
        print("Error calculating pay period earnings from shifts: ", e)
    try:        
        print("\nHere are the pay period details for the selected pay period:")
        print("***************************************************************************")
        print(f'Pay Period: {format_payperiod(payperiod_obj)}')

        print(f'\nEarnings               rate           hours/units            this period')
        print(f'Regular:               {wage}              {round(regular_hours,2)}                   {round(wage * regular_hours,2)}')
        print(f'Overtime:              {overtime_wage}             {round(overtime_hours,2)}                     {round(overtime_wage * overtime_hours, 2)}')
        print(f'Credit card tips owed:                   0.00                    {round(cc_tips, 2)}')
        print(f'\n                        Gross Pay                              ${round((wage*regular_hours)+(overtime_wage*overtime_hours)+cc_tips,2)}')
        print(f'                      + Cash tips paid out.....................${cash_tips}')
        print("\n***************************************************************************")
    except Exception as e:
        print("Error calculating pay period earnings: ", e)
        print("Make sure wage is a number with no more than two decimal places.")
        
def format_shift(shift):
    return f'{shift._month}/{shift._day}/{shift._year} | Hours: {hours_worked(shift)} hours | Tips: ${shift._cc_tip + shift._cash_tip}'

def get_shifts(payperiod_obj):
    shifts = payperiod_obj.shifts()
    return shifts

def enumerate_shifts(selected_payperiod, shifts):
    print(f'\nShifts in Pay Period: {format_payperiod(selected_payperiod)}')
    print("*************************************************")
    if shifts:
        for i, shift in enumerate(shifts, start=1):
            print(f'{i}. {format_shift(shift)}')
    else:
        print("\nNo shifts recorded.")
    print("\n*************************************************")    

def display_shift_details(shift_obj):
    print(f'\nSHIFT DETAILS ON: {shift_obj._month}/{shift_obj._day}/{shift_obj._year}')
    print("**************************")
    print(f'\nClock In Time: {shift_obj._clock_in}')
    print(f'Clock Out Time: {shift_obj._clock_out}')
    print(f'Hours Worked: {hours_worked(shift_obj)} hours')
    print(f'\nCredit Card Tips: ${shift_obj._cc_tip}')
    print(f'Cash Tips: ${shift_obj._cash_tip}')
    print(f'Total Tips: ${shift_obj._cc_tip + shift_obj._cash_tip}')
    print("\n**************************")


def create_shift(payperiod_id):
    print("\nShift Date:")
    month = input("Enter month (1-12): ")
    day = input("Enter day (1-31): ")
    year = input("Enter year (YYYY): ")
    print("\nTime In/Out (Time must be in HH:MM 24-hour format):")
    clock_in = input("Enter clock-in time: ")
    clock_out = input("Enter clock-out time: ")
    print("\nTips (Tip must be a 0 or positive number with up to two decimals):")
    cc_tip = input("Enter credit card tips earned: $")
    if not cc_tip: cc_tip = 0
    cash_tip = input("Enter cash tips earned: $")
    if not cash_tip: cash_tip = 0

    try:
        shift = Shift.create(int(month), int(day), int(year), clock_in, clock_out, float(cc_tip), float(cash_tip), payperiod_id)
        print(f'\nSuccess: {format_shift(shift)}')
    except Exception as e:
        print("\nError creating shift: ", e)

def update_shift(shift_obj):
    try:
        print("\nEnter the updated shift information or hit <enter> to leave it as is!")
        print("\nShift Date:")
        month = input(f"Current month: {shift_obj._month} | New month (1-12): ")
        if month: shift_obj.month = int(month)
        day = input(f"Current day: {shift_obj._day} | New day (1-31): ")
        if day: shift_obj.day = int(day)
        year = input(f"Current year: {shift_obj._year} | New year (YYYY): ")
        if year: shift_obj.year = int(year)
        print("\nTime In/Out (Time must be in HH:MM 24-hour format):")
        clock_in = input(f"Current time in: {shift_obj._clock_in} | New clock-in time: ")
        if clock_in: shift_obj.clock_in = clock_in
        clock_out = input(f"Current time out: {shift_obj._clock_out} | New clock-out time: ")
        if clock_out: shift_obj.clock_out = clock_out
        print("\nTips (Tip must be a 0 or positive number with up to two decimals):")
        cc_tip = input(f"Current CC tips: {shift_obj._cc_tip} | New credit card tips: $")
        if cc_tip: shift_obj.cc_tip = float(cc_tip)
        cash_tip = input(f"Current cash tips: {shift_obj._cash_tip} | New cash tips: $")    
        if cash_tip: shift_obj.cash_tip = float(cash_tip)

        shift_obj.update()
        print(f"\nSuccess: {format_shift(shift_obj)}")
    except Exception as e:
        print("\nError updating shift: ", e)

def delete_shift(shift_obj):
    try:
        shift_obj.delete()
        print(f'\nShift deleted successfully: {format_shift(shift_obj)}')
    except Exception as e:
        print("\nError deleting shift: ", e)    

def hours_worked(shift_obj):
    """Calculate hours worked as a decimal number."""
    h_in, m_in = map(int, shift_obj._clock_in.split(":"))
    h_out, m_out = map(int, shift_obj._clock_out.split(":"))

    total_minutes = (h_out * 60 + m_out) - (h_in * 60 + m_in)
    if total_minutes < 0:
        raise ValueError("Clock-out time must be after clock-in time")

    return round(total_minutes / 60, 2)