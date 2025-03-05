# lib/cli.py

from helpers import (
    exit_program,
    create_shift,
    view_all_shifts,
    view_shifts_in_payperiod,
    view_shifts_in_date_range,
    earnings_by_payperiod
)

def main_menu():
    '''Main menu for the earnings tracker'''

    choice = 0
    while choice != 4:

        print("***PERSONAL EARNINGS MANAGER***")
        print("Hello...")
        print('''Please choose from the following: ''')
        print("1 - LOG A SHIFT")
        print("2 - VIEW PAST SHIFTS")
        print("3 - CALCULATE EARNINGS")
        print("4 - EXIT")

        choice = int(input(">>> "))
        
        if choice == 1:
            create_shift()

        elif choice == 2:
            shifts_menu()

        elif choice == 3:
            earnings_menu()

        

        else:
            print("Invalid choice. Please enter a number from 1-4")

    exit_program()


def shifts_menu():
    ''' Menu for viewing past shifts '''

    choice = 0
    while choice != 4:

        print("***VIEW PAST SHIFTS***")
        print("1 - VIEW ALL SHIFTS")
        print("2 - VIEW SHIFTS BY PAY PERIOD")
        print("3 - VIEW SHIFTS BY DATE RANGE")
        print("4 - BACK TO MAIN MENU")

        choice = int(input(">>> "))

        if choice == 1:
            view_all_shifts()
            # should they be able to select a shift? 
            # options to view more? 
            # option to select a shift - edit, calculate something, delete

        elif choice == 2:
            view_shifts_in_payperiod()
            # can add, edit, delete, or view more info for shift

        elif choice == 3:
            view_shifts_in_date_range()
            # helper fn - enter start and end date to display
        
        else:
            print("Invalid choice. Please enter a number from 1-4")
    
    main_menu()

def earnings_menu():
    ''' Menu for calculating earnings '''

    choice = 0
    while choice != 3:

        print("***CALCULATE EARNINGS***")
        print("1 - CALCULATE EARNINGS BY PAY PERIOD")
        print("2 - CALCULATE EARNINGS BY DATE RANGE")
        print("3 - BACK TO MAIN MENU")

        choice = int(input(">>> "))

        if choice == 1:
            earnings_by_payperiod()

        elif choice == 2:
            earnings_in_date_range()

        elif choice == 3:
            break

        else:
            print("Invalid choice. Please enter a number from 1-3")

if __name__ == "__main__":
    main_menu()

## PAY PERIOD
# go into a particular pay period which will show existing shifts
# within the pay period you can delete it, add a new shift, or view more details... total hours, total tips, wage, hourly wage(w tips), avg tipout, id for existing shift...
##SHIFT
# within each shift you can edit, delete, view - clock in, clock out, wage, total hours, tips - hourly wage(w tips)

#Pay period
## start month, day, year
## end month, day, year
## wage class attribute


# ***PERSONAL EARNINGS TRACKER***
# MAIN MENU
# 1 - SHIFTS - i want to be able to view, edit, delete, or add a new shift
# 2 - PAY PERIODS - i want to view
# 3 - MONTH
# 4 - YEAR
# E - EXIT

    # > SHIFTS
    ## shows shifts
    # 1 - ADD SHIFT
    # 2 - VIEW SHIFT DETAILS - enter date
    # 3 - GO BACK TO MAIN MENU

        # >> VIEW SHIFTS
        #somehow selects a shift
        # 1 - Hours/Wage
        # 2 - Tips
        # 3 - Avg hourly wage with tips
        # 4 - 


    ## > PAY PERIODS
    ## shows pay periods
    # 1 - VIEW PAY PERIOD
    # 2 - ADD A PAY PERIOD
    # 3 - GO BACK TO MAIN MENU