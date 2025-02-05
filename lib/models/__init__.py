import sqlite3

CONN = sqlite3.connect('earnings.db')
CURSOR = CONN.cursor()