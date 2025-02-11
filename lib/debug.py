#!/usr/bin/env python3
# lib/debug.py

from models.payperiod import PayPeriod
from models.shift import Shift

# def reset_database():
#     PayPeriod.drop_table()
#     PayPeriod.create_table()


# reset_database()
shift = Shift(25, 1, 23, "4:47 PM", "9:28 PM", 100.00, 10)      
shift.__repr__()
shift.clock_out = "5:23 PM"
shift.clock_in = "4:30 PM"

payperiod = PayPeriod(25, 1, 16, 25, 1, 27)

breakpoint()