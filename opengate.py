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
        print("Invalid command, h to show available commands.")
        return
    f = switcher[action]
    f()


def main():

    # start sqlite connection
    connection = conn('test_database.db')
    c = connection.cursor()
    c.execute(q.create_table)
    c.execute(q.insert_dummy_values)
    # clear screen
    a.clear_screen()
    for row in c.execute(q.get_all):
        pprint(f'[test]: row is: {row}')
    # Display info, and take input
    print(constants.title_text)
    while(not s.stop):
        act(poll())
    clean(connection)


# call to main, start the program lol
main()
