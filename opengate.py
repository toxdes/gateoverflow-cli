import sqlite3
from pprint import pprint
import queries as q
connection = sqlite3.connect('test.db')

c = connection.cursor()
c.execute(q.create_table)
c.execute(q.insert_dummy_values)

for row in c.execute(q.get_all):
    pprint(f'row is: {row}')
