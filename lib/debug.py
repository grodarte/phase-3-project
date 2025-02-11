#!/usr/bin/env python3
# lib/debug.py

from models.payperiod import PayPeriod
from models.shift import Shift

def reset_database():
    PayPeriod.drop_table()
    PayPeriod.create_table()


reset_database()


breakpoint()