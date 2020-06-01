# libs
import sqlite3
from pprint import pprint
import os
import sys
import random as r
import pathlib
from configparser import ConfigParser
import toml
# local imports
from gateoverflow import queries as q
from gateoverflow import __version__
from gateoverflow import constants
from gateoverflow import actions as a
from gateoverflow.state import state as s
from gateoverflow.logger import d
from gateoverflow.helpers import crawl_metadata, uncrawled_metadata_count, parse_cmd, prettify_table, print_logo, ask, latest_version_check
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
    # requires python >= 3.5 for now
    # TODO: make it work for lower python versions, and windows
    # TODO: check if project_home is writable
    config_file = Path.joinpath(project_home, f'config.toml')
    db_file = Path.joinpath(project_home, f'{s["database_name"]}')
    # home folder may not exists, in that case it's a fresh start
    if not Path.exists(project_home):
        # it is a fresh start
        print("It appears you are running this program for the first time, so I need to configure.")
        print("Creating Project directory...")
        Path.mkdir(project_home, exist_ok=True, parents=True)
        d('t', 'created path')

    # config file may not exist
    if not Path.exists(config_file):
        print('Creating default config...')
        # FIXME: use sample_config.toml instead of this string representation
        config_file.write_text(constants.sample_config)
        d('t', 'wrote sample config.')
        print(
            f"Config file created at {str(config_file)}.\nYou can modify it according to your taste.")
    # load the config into state
    # parse the config file if exists, fallback to default ones.
    # TODO: parser should differenciate types, such as integers for numbers and strings
    # TODO: support utf-8 for config file
    try:
        user_config = toml.load(str(config_file))
        d("t", "successfully loaded config file into an object")
    except Exception as e:
        d(print, f'{e}')
        print("user config is invalid.")
        a.abort_program()
    # load the relevant config into state
    # TODO: hacky solution, improve this parser later
    for key in user_config:
        if key not in s.keys():
            continue
        s[key] = user_config[key]
        d(print, f'Config: key: {key}, value: {user_config[key]}')
    d('t', 'user config loaded into state')
    db_file = Path.joinpath(project_home, f'{s["database_name"]}')
    if not Path.exists(db_file):
        print("No default database found.")
        print("Creating a brand new database...")
        if(ask()):
            # Create a database
            s['db_path'] = str(db_file)
        else:
            print(
                "Okay. There's no database, you should copy your *.db file to ${project_home}")
    s['project_home'] = project_home

    if Path.exists(db_file):
        s["db_path"] = str(db_file)


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
    c.execute(q.get_user)
    res = c.fetchone()
    if res == None:
        d('t', "res is none for q.get_user")
        print("You haven't added your details yet.")
        print("Please give me your username, and name...")
        if(ask()):
            username = input('Enter Username: ')
            name = input('Enter Name: ')
            if(len(username) > 0 and len(name) > 0):
                s['user'] = constants.User(username, name)
                c.execute(q.create_user, [username, name])
                d('t', 'added user info after asking the same to the user')
        else:
            d('t', 'user refused to give username and name')
            print("Fine, stay anonymous then")
            s['user'] = constants.User()
    else:
        d('t', 'res is not null')
        d(print, f'{res}')
        res = [str(each) for each in res]
        s['user'] = constants.User(res[1], res[0])
    # c.executescript(q.insert_dummy_values)
    a.clear_screen()
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
    # TODO: use argparse here
    if(len(sys.argv) >= 2):
        for each in sys.argv:
            if(each == '-d' or each == '--debug'):
                s['DEBUG'] = True
            if(each == '-v' or each == '-version' or each == '--version'):
                print(f'gateoverflow-cli v{__version__}')
                latest_version_check()
                exit(int(0))
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
