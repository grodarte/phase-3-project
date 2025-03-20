# lib/cli.py

from helpers import (
    exit_program,
    get_payperiods,
    enumerate_payperiods,
    create_payperiod,
    update_payperiod,
    calculate_payperiod_earnings,
    get_shifts,
    enumerate_shifts,
    display_shift_details,
    create_shift,
    update_shift,
    delete_shift
)

def main_menu():
    '''MAIN MENU FOR EARNINGS TRACKER'''
    choice = ''

    while choice != 'e':
        print("*** PERSONAL EARNINGS MANAGER ***")
        print('''\nPlease choose from the following: ''')
        print("\nType P or p to view the PAY PERIODS")
        print("OR type E or e to EXIT")
        choice = input("\n>>> ").strip().lower()

        if choice == 'p':
            show_payperiods_menu()
        elif choice != 'e':
            print("\nInvalid choice, please try again.")

    exit_program()

def show_payperiods_menu():
    '''Menu for interacting with payperiods'''
    choice = ''

    while choice != 'b':
        payperiods = get_payperiods()
        enumerate_payperiods(payperiods)
        print("\nPlease select the number of the pay period to see shifts/calculate earnings")
        print("             OR")
        print("Type A or a to ADD a new Pay period")
        print("Type B or b to go BACK to previous menu")
        print("Type E or e to EXIT the program")

        choice = input("\n>>> ").strip().lower()

        if choice.isdigit():
            choice_num = int(choice)
            if choice_num in range(1, len(payperiods) + 1):
                selected_payperiod = payperiods[choice_num - 1]
                show_shifts_menu(selected_payperiod)
            else:
                print(f'\nInvalid pay period selection, please try again.')
        elif choice == 'a':
            create_payperiod()
        elif choice == 'e':
            exit_program()
        elif choice != 'b':
            print("\nInvalid choice, please try again.")

def show_shifts_menu(selected_payperiod):
    '''Menu for interacting with shifts'''
    choice = ''

    while choice != 'b':
        shifts = get_shifts(selected_payperiod)
        enumerate_shifts(selected_payperiod, shifts)
        print("\nPlease select the number of the shift to see details")
        print("               OR")
        print("Type A or a to ADD a new shift to this pay period")
        print("Type U or u to UPDATE this pay period's dates")
        print("Type C or c to CALCULATE this pay period's total hours/earnings")
        print("Type B or b to go BACK to previous menu")
        print("Type E or e to EXIT the program")

        choice = input("\n>>> ").strip().lower()

        if choice.isdigit():
            choice_num = int(choice)
            if choice_num in range(1, len(shifts) + 1):
                selected_shift = shifts[choice_num - 1]
                selected_shift_menu(selected_shift)
            else:
                print("\nInvalid shift selection, please try again.")
        elif choice == 'a':
            create_shift(selected_payperiod.id)
        elif choice == 'u':
            update_payperiod(selected_payperiod)
        elif choice == 'c':
            minimum_wage = 16.50
            print("\nEnter your wage or hit <enter> to proceed with earnings calculations at minimum wage (${minimum_wage})")
            wage_input = input("\n ")
            print("\nWage must be a positive number with up to two decimal places")
            calculate_payperiod_earnings(selected_payperiod)
        elif choice == 'e':
            exit_program()
        elif choice != 'b':
            print("\nInvalid choice, please try again.")

def selected_shift_menu(selected_shift):
    choice = ''

    while choice != 'b':
        display_shift_details(selected_shift)
        print("\nPlease choose from the following:")
        print("\nType U or u to UPDATE this shift")
        print("Type D or d to DELETE this shift")
        print("Type B or b to go BACK to the previous menu")
        print("Type E or e to EXIT the program")

        choice = input("\n>>> ").strip().lower()

        if choice == 'u':
            update_shift(selected_shift)
        elif choice == 'd':
            delete_shift_menu(selected_shift)
            choice = 'b'
        elif choice == 'e':
            exit_program()
        elif choice != 'b':
            print("\nInvalid choice, please try again.")

def delete_shift_menu(selected_shift):
    choice = ''

    while choice != 'n':
        print("\n*** WARNING: Deleting shift cannot be undone ***")
        print("\nAre you sure you want to delete shift?")
        print("\nType Y or y for Yes")
        print("Type N or n for No")

        choice = input("\n>>> ").strip().lower()

        if choice == 'y':
            delete_shift(selected_shift)
            choice = 'n'
        elif choice != 'n':
            print("\nInvalid choice, please try again.")

if __name__ == "__main__":
    main_menu()