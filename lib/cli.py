# lib/cli.py

from helpers import (
    exit_program,
    list_payperiods,
)

def main_menu():
    '''Main menu for the earnings tracker'''

    choice = ''
    exit_choice = 'e'

    while choice != exit_choice:
        print("***PERSONAL EARNINGS MANAGER***")
        print("Hello...")
        print('''Please choose from the following: ''')
        print("Type P or p to view PAY PERIODS")
        print("OR type E or e to exit")

        choice = input(">>> ")
        if choice == 'p':
            list_payperiods()
        else:
            print("Invalid choice, please try again.")

    exit_program()

def payperiods_menu():
    '''Menu for interacting with payperiods'''

    choice = 0
    while choice != 4:

        print()






if __name__ == "__main__":
    main_menu()