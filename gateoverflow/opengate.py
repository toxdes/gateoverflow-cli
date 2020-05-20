# libs
import sqlite3
from pprint import pprint
import os
import sys
import random as r
import pathlib
from configparser import ConfigParser
# local imports
from gateoverflow import queries as q
from gateoverflow import constants
from gateoverflow import actions as a
from gateoverflow.state import state as s
from gateoverflow.logger import d
from gateoverflow.helpers import crawl_metadata, uncrawled_metadata_count, parse_cmd, prettify_table, print_logo, ask
modes = constants.modes


def conn(name):
    return sqlite3.connect(name)


def clean(con):
    con.close()


def poll():
    symbol = s['shell_symbol']
    prefix = ''
    if s['DEBUG'] == True:
        prefix = f'[debug-mode]'
    if s["mode"] != modes.DEFAULT:
        prefix = f'{prefix}[{s["mode"]}]'
    symbol = f'{prefix}{symbol}'
    action = input(symbol)
    return action


def act(cmd):
    # do something based on action
    action = cmd.lower().split(' ')[0]
    switcher = s["switcher"]
    err, questions, tags, parser_action = parse_cmd(cmd)
    if not err:
        s["questions_list"] = questions
        s["tags"] = tags
        s["parser_action"] = parser_action
        action = 'parser'

    if action == 'ls':
        if(len(cmd.split(' ')) > 1):
            s["list_string"] = cmd
        else:
            s["list_string"] = f'ls {s["how_many"]}'

    d(print, f'action: {action}')
    if action not in switcher.keys():
        action = 'invalid'
    f = switcher[action]
    f()


def database_exists():
    return pathlib.Path.joinpath(s['project_home'], s['database_name']).is_file()


def startup_routine():
    Path = pathlib.Path
    # check if the appData directory exists, create it if it doesn't exist, and should be writable
    home_dir = Path.home()
    project_home = Path.joinpath(
        home_dir, f'.{constants.project_name}')
    # TODO: fuck this, json is good enough, complete tomorrow.
    config_file = Path.joinpath(project_home, f'config')
    db_file = Path.joinpath(project_home, f'{s["database_name"]}')
    # requires python >= 3.5 for now
    # TODO: make it work for lower python versions, and windows
    # TODO: check if project_home is writable
    if not Path.exists(project_home):
        # it is a fresh start
        print("It appears you are running this program for the first time, so I need to configure.")
        print("Creating Project directory...")
        Path.mkdir(project_home, exist_ok=True, parents=True)
        d('t', 'created path')
        print('Creating new config...')
        if not Path.exists(config_file):
            # create default config file
            # f = open(str(config_file), 'r+')
            config_file.write_text(constants.default_config)
            d('t', 'wrote default config to file')
            print(
                f"Config file created at {str(config_file)}.\nYou can modify it according to your taste.")
        if not Path.exists(db_file):
            print("No default database found.")
            print("Creating a brand new database...")
            if(ask()):
                # Create a database
                s['db_path'] = db_file
                username = input('Your Username:')
                name = input('Your Name:')
                s['user'] = constants.User(username, name)
                pass
            else:
                print(
                    "Okay. There's no database, you should copy your *.db file to ${project_home}")
    s['project_home'] = project_home

    # config file may not exist
    if not Path.exists(config_file):
        config_file.write_text(constants.default_config)

    if Path.exists(db_file):
        s["db_path"] = str(db_file)
    # parse the config file if exists, fallback to default ones.
    # TODO: parser should differenciate types, such as integers for numbers and strings
    parser = ConfigParser()
    parser.read(config_file)
    d("t", "created parser, because config file was existing already")
    # load the relevant config into state
    # TODO: hacky solution, improve this later
    loaded = parser['DEFAULT']
    for key in loaded:
        s[key] = loaded.get(key)
        d(print, f'Config: key: {key}, value: {parser["DEFAULT"][key]}')


def main():
    a.clear_screen()
    try:
        startup_routine()
    except Exception as e:
        print("Startup failed.")
        d(print, f'{e}')
        a.abort_program()
    if s["project_home"] == None:
        print("No place to store my things.")
        a.abort_program()
    # start sqlite connection
    if s["db_path"] == None:
        print("No database found. Creating a brand new database...")
        if(ask()):
            s["db_path"] = str(pathlib.Path.joinpath(
                s["project_home"], f'{s["database_name"]}'))
        else:
            print(
                f'I cannot run without a database, please create on, or copy already existing *.db file to {s["project_home"]}')
            a.abort_program()
        # print('deleting for ease of development')
        # os.system(f'rm {constants.database_name}')
    connection = conn(s['db_path'])
    s['conn'] = connection
    s['cursor'] = connection.cursor()
    c = connection.cursor()
    c.executescript(q.create_tables)
    try:
        c.executescript(q.alter_tables)
    except:
        d(print, "No need to alter tables.")
    c.executescript(q.create_triggers)
    c.executescript(q.create_default_tags)
    res = c.execute(q.get_user)
    if res == None:
        print("You haven't added your details yet.")
        print("Please give me your username, and name...")
        if(ask()):
            username = input('Enter Username: ')
            name = input('Enter Name: ')
            if(len(username) > 0 and len(name) > 0):
                s['user'] = constants.User(username, name)
                c.execute(q.create_user, [username, name])
        else:
            print("Fine, stay anonymous then")
        s['user'] = constants.User()
    else:
        d('t', 'res is not null')
        for row in res:
            res = [str(each) for each in row]
            d(print, f'{res[0]} | {res[1]}')
            s['user'] = constants.User(res[0], res[1])
            break
    # c.executescript(q.insert_dummy_values)
    # a.open_questions()
    # clear screen
    # a.clear_screen()
    s['switcher'] = a.get_switcher()
    for row in c.execute(q.get_all):
        d(pprint, f'[test]: row is: {row}')
    # Display info, and take input
    while(not s['stop']):
        act(poll())
    connection.commit()
    clean(connection)


def start():
    # for starting cli with debug = true by passing -d or --debug
    if(len(sys.argv) >= 2):
        for each in sys.argv:
            if(each == '-d' or each == '--debug'):
                s['DEBUG'] = True
                break
    if s['DEBUG'] == True:
        main()
    else:
        try:
            main()
        except:
            print('I am the one who gets to say sorry here.')
            a.abort_program()


'''
def main():
    connection = conn(constants.database_name)
    s['cursor'] = connection.cursor()
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
