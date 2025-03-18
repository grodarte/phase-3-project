#!/usr/bin/env python3
# lib/debug.py

from models.payperiod import PayPeriod
from models.shift import Shift

def reset_database():
    PayPeriod.drop_table()
    PayPeriod.create_table()
    Shift.drop_table()
    Shift.create_table()

    #Create seed data
    novemberfirst = PayPeriod.create(2025,10,14,2025,10,27)
    novembersecond = PayPeriod.create(2025,10,28,2025,11,10)
    Shift.create(2025,10,14,"11:32","18:48",139.36,0, novemberfirst.id)
    Shift.create(2025,10,15,"15:29","21:10", 94.82, 0, novemberfirst.id)
    Shift.create(2025,10,28,"16:52","21:59", 131.72, 0, novembersecond.id)
    Shift.create(2025,10,29,"16:00", "22:21", 186.21, 0, novembersecond.id)


reset_database()



breakpoint()