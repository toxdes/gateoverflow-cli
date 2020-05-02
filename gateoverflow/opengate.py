# libs
import sqlite3
from pprint import pprint
import os
import sys
import random as r
# local imports
from gateoverflow import queries as q
from gateoverflow import constants
from gateoverflow import actions as a
from gateoverflow import state as s
from gateoverflow.logger import d
from gateoverflow.helpers import crawl_metadata, uncrawled_metadata_count, parse_cmd, prettify_table, print_logo
modes = constants.modes


def conn(name):
    return sqlite3.connect(name)


def clean(con):
    con.close()


def poll():
    symbol = constants.shell_symbol
    prefix = ''
    if s.DEBUG == True:
        prefix = f'[debug-mode]'
    if s.mode != modes.DEFAULT:
        prefix = f'{prefix}[{s.mode}]'
    symbol = f'{prefix}{symbol}'
    action = input(symbol)
    return action


def act(cmd):
    # do something based on action
    action = cmd.lower().split(' ')[0]
    switcher = s.switcher
    err, questions, tags, parser_action = parse_cmd(cmd)
    if not err:
        s.questions_list = questions
        s.tags = tags
        s.parser_action = parser_action
        action = 'parser'

    if action == 'ls':
        if(len(cmd.split(' ')) > 1):
            s.list_string = cmd
        else:
            s.list_string = f'ls {s.how_many}'

    d(print, f'action: {action}')
    if action not in switcher.keys():
        action = 'invalid'
    f = switcher[action]
    f()


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
    s.conn = connection
    s.cursor = connection.cursor()
    c = connection.cursor()
    c.executescript(q.create_tables)
    c.executescript(q.create_triggers)
    c.executescript(q.create_default_tags)
    # c.executescript(q.insert_dummy_values)
    # a.open_questions()
    # clear screen
    # a.clear_screen()
    s.switcher = a.get_switcher()
    for row in c.execute(q.get_all):
        d(pprint, f'[test]: row is: {row}')
    # Display info, and take input
    a.clear_screen()
    while(not s.stop):
        act(poll())
    connection.commit()
    clean(connection)


def start():
    # for starting cli with debug = true by passing -d or --debug
    if(len(sys.argv) >= 2):
        for each in sys.argv:
            if(each == '-d' or each == '--debug'):
                s.DEBUG = True
                break
    if s.DEBUG == True:
        main()
    else:
        try:
            main()
        except:
            print('I am the one who gets to say sorry here.')
            a.exit_program()


'''
def main():
    connection = conn(constants.database_name)
    s.cursor = connection.cursor()
    uncrawled_metadata_count()
    crawl_metadata()
    connection.commit()
'''

# call to main, start the program lol
# try:
#     main()
# except:
#     print("\nI think I'm the one who says sorry here.")
#     a.exit_program()
