# libs
import sqlite3
from pprint import pprint

# local imports
import queries as q
import constants
import actions as a
import state as s


def conn(name):
    return sqlite3.connect(name)


def clean(con):
    con.close()


def poll():
    action = input(constants.shell_symbol)
    return action


def act(action):
    # do something based on action
    action = action.lower()
    switcher = a.switcher
    print(f'action: {action}')
    if action not in switcher.keys():
        print("Invalid command.")
        return
    f = switcher[action]
    f()


def main():
    # Display info, and take input
    print(constants.title_text)
    poll()
    # start sqlite connection
    connection = conn('test_database.db')
    c = connection.cursor()
    c.execute(q.create_table)
    c.execute(q.insert_dummy_values)
    for row in c.execute(q.get_all):
        pprint(f'row is: {row}')
    while(not s.stop):
        act(poll())
    clean(connection)


main()
