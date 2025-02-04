# lib/cli.py

from helpers import (
    exit_program,
    helper_1
)

def main():

    payPeriods = []

    choice = 0
    while choice != 4:
        print("*** Pay Period Manager ***")
        print("1. Add a pay period")
        print("2. Lookup a pay period")
        print("3. Display pay periods")
        print("4. Quit")
        choice = int(input())

if __name__ == "__main__":
    main()

# add multiple layered loops
#NAME
## PAY PERIOD
# go into a particular pay period which will show existing shifts
# within the pay period you can delete it, add a new shift, or view more details... total hours, total tips, wage, hourly wage(w tips), avg tipout, id for existing shift...
##SHIFT
# within each shift you can edit, delete, view - clock in, clock out, wage, total hours, tips - hourly wage(w tips)