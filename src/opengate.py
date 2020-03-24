# libs
import sqlite3
from pprint import pprint
import os
import random as r
# local imports
import queries as q
import constants
import actions as a
import state as s
from logger import d
from helpers import crawl_metadata, uncrawled_metadata_count
modes = constants.modes


def conn(name):
    return sqlite3.connect(name)


def clean(con):
    con.close()


def poll():
    symbol = constants.shell_symbol
    if s.mode != modes.DEFAULT:
        prefix = f'[{s.mode}]'
        symbol = f'{prefix}{symbol}'
    action = input(symbol)
    return action


def act(cmd):
    # do something based on action
    action = cmd.lower().split(' ')[0]
    switcher = s.switcher
    err, all_nums = list_of_ints(action)
    if not err:
        print('Number(s) found, treating them as questionIDs, and opening each in web-browser...')
        s.questions_list = all_nums
        action = 'open'
    if action == 'ls' or 'list':
        if(len(cmd.split()) <= 1):
            pass
        else:
            s.list_string = cmd

    print(f'action: {action}')
    if action not in switcher.keys():
        print("Invalid command, h to show available commands.")
        return
    f = switcher[action]
    f()


def list_of_ints(in_str):
    error = False
    nums = []
    try:
        nums = [int(a) for a in in_str.split(',')]
    except:
        error = True
    return (error, nums)


def database_exists():
    return os.path.isfile(constants.database_name)


def main():

    # start sqlite connection
    if database_exists():
        d(print, 'database already exists.')
        # print('deleting for ease of development')
        # os.system(f'rm {constants.database_name}')
    else:
        d(print, 'fresh start, creating database.')
    connection = conn(constants.database_name)
    s.cursor = connection.cursor()
    c = connection.cursor()
    c.executescript(q.create_tables)
    c.executescript(q.create_triggers)
    # c.executescript(q.insert_dummy_values)
    # a.open_questions()
    # clear screen
    # a.clear_screen()
    s.switcher = a.get_switcher()
    for row in c.execute(q.get_all):
        d(pprint, f'[test]: row is: {row}')
    # Display info, and take input
    print(constants.title_text)
    while(not s.stop):
        act(poll())
    connection.commit()
    clean(connection)


'''
def main():
    connection = conn(constants.database_name)
    s.cursor = connection.cursor()
    uncrawled_metadata_count()
    crawl_metadata()
    connection.commit()
'''

# call to main, start the program lol
main()