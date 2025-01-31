# lib/cli.py

from helpers import (
    exit_program,
    helper_1
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            helper_1()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Some useful function")


if __name__ == "__main__":
    main()

# add multiple layered loops
#NAME
## PAY PERIOD
# go into a particular pay period which will show existing shifts
# within the pay period you can delete it, add a new shift, or view more details... total hours, total tips, wage, hourly wage(w tips), avg tipout, id for existing shift...
##SHIFT
# within each shift you can edit, delete, view - clock in, clock out, wage, total hours, tips - hourly wage(w tips)