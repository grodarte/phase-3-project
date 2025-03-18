# lib/cli.py

from helpers import (
    exit_program,
    list_payperiods,
)

def main_menu():
    '''Main menu for the earnings tracker'''

    choice = 0
    while choice != 2:

        print("***PERSONAL EARNINGS MANAGER***")
        print("Hello...")
        print('''Please choose from the following: ''')
        print("1 - View Pay Periods")
        print("2 - Exit")

        choice = int(input(">>> "))
        
        if choice == 1:
            pass
            list_payperiods()

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