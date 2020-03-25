import os
import webbrowser
import state as s
import constants
from logger import d
from helpers import readable_date, open_link, uncrawled_metadata_count, crawl_metadata, print_table
modes = constants.modes


def exit_program():
    if (s.mode == modes.OPEN_MODE):
        print("Exiting open_mode...")
        s.mode = modes.DEFAULT
        return
    print("Okay, bye.")
    s.stop = True


def print_help():
    print("Commands - ")
    for each in switcher.keys():
        try:
            print(f'\t{each}\t-\t{ switcher_help[each]}')
        except:
            print(f"Help not available for command: {each}")


def clear_screen():
    cmd = 'clear' if os.name == 'posix' else 'cls'
    os.system(cmd)
    print(constants.title_text)


def open_mode():
    if(s.mode == modes.OPEN_MODE):
        print("Already in open mode.")
        return
    s.mode = modes.OPEN_MODE


def debug_toggle():
    res = ''
    if s.DEBUG == True:
        s.DEBUG = False
        res = 'OFF'
    else:
        s.DEBUG = True
        res = 'ON'
    print(f'debug mode is {res}')


def do_nothing():
    pass
# actions switcher
# TODO: Find a better way to structure this

# give switcher based on the active mode


def get_switcher():
    switchers = {
        modes.DEFAULT: switcher,
        modes.OPEN_MODE: open_mode_switcher
    }
    return switchers[s.mode]


def open_questions():
    # get the input list, stored in state
    question_ids = s.questions_list
    # insert into recent questions table, along with timestamp, update visited count if already visited
    c = s.cursor
    for each in question_ids:
        # check if already exists
        c.execute("SELECT * FROM recents WHERE question_id=?", [each])
        res = c.fetchone()
        if res != None:
            # update
            c.execute("UPDATE recents SET visited_count=(SELECT visited_count FROM recents WHERE question_id=?)+1  where question_id=?", [
                      each, each])
        else:
            # insert
            c.execute("INSERT INTO recents(question_id) values(?)", [each])
        open_link(f'https://gateoverflow.in/{each}')


def list_command():
    list_options = set(['r', 'q', 't', 'recent', 'questions', 'tags'])
    row_offset = 0
    cmd = s.list_string.split(' ')
    c = s.cursor
    d(print, 'lists different things here')
    d(print, f'probably, you wanted to list: {cmd}')
    if len(cmd) <= 1 or cmd[1] not in list_options:
        d(print, 'Invalid option')
        d(print, switcher_help['ls'])
        return
    how_many = None
    try:
        how_many = cmd[2]
    except:
        how_many = s.how_many
    what_to_show = cmd[1]
    d(print, f"omg you want this? : {what_to_show}, {how_many} items")
    table = None
    if what_to_show in ['recent', 'r']:
        table = 'recents'
    elif what_to_show in ['questions', 'q']:
        table = 'questions'
    elif what_to_show in ['tags', 't']:
        table = 'tags'
    else:
        d(print, "I shouldn't be here")
        return
    if table == 'recents':
        q = f"SELECT question_id, visited_count, last_visited FROM {table} ORDER BY last_visited ASC, visited_count DESC  LIMIT {how_many} OFFSET {row_offset}"
        c.execute(q, [])
        res = c.fetchall()
        # title = 'QuestionID'.ljust(12) + 'Visited'.ljust(12) + 'Time'.ljust(12)
        # print(title)
        headers = ['Question ID', 'Visited', 'Time']
        data = []
        for row in res:
            row = [str(each) for each in row]
            data.append([row[0], row[1], readable_date(row[2])])
        print_table(data, headers)
    else:
        d(print, "not implemented yet.")


def crawler():
    count = uncrawled_metadata_count()
    print(f'Unscraped records: {count}')
    q = input("Do you want to continue?(yes/no) (default: no): ")
    if(q.lower() == 'yes' or q.lower() == 'y'):
        # continue
        crawl_metadata()
    else:
        print('Abort.')
        return


# default mode switcher
switcher = {
    '': do_nothing,
    'q': exit_program,
    'h': print_help,
    'o': open_mode,
    'ls': list_command,
    'crawler': crawler,
    'debug-toggle': debug_toggle,
    'quit': exit_program,
    'help': print_help,
    'clear': clear_screen,
    'open-mode': open_mode,
    'open': open_questions,
    'list': list_command
}

open_mode_switcher = {
    '': do_nothing,
    'q': exit_program,
    'h': print_help,
    'quit': exit_program,
    'help': print_help,
    'open': open_questions,
}
# help description for each action
switcher_help = {
    'q': "Alias to quit. Exit the program normally.",
    'h': "Alias to help. Shows available commands.",
    'o': "Alias to open-mode. Go into open-mode.",
    'ls': "Alias to list. List things. Usage: ls [recents(r)(default) | tags(t) | questions(q)] [number (default:10)]",
    'quit': "Exit the program normally.",
    'help': "Shows available commands.",
    'clear': "Clear output screen.",
    'open-mode': "Go into open-mode.",
    'debug-toggle': "Toggle debug output.",
    'open': 'if a number, or multiple comma separated numbers are provided, without any command, each one will be treated as question ID, and will be opened in browser.',
    'list': " List things. Usage: ls [recent(r) | tags(t) | questions(q)] [number]",
    'crawler': "Start crawling for unscraped information about recently opened questions."
}


# possible alternative to switcher structure
'''
action = {
    '_id':'unique',
    'action_call':'call, what to do',
    'alias':'what an alias is',
    'help_text':'wow'
}
'''
