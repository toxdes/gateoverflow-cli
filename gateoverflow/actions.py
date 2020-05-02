import os
from gateoverflow import state as s
from gateoverflow import constants
from gateoverflow.logger import d
from gateoverflow.helpers import readable_date, open_link, uncrawled_metadata_count, crawl_metadata, prettify_table, print_logo
modes = constants.modes


def exit_program():
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
    print_logo()


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
    print('Done!')


def list_command():
    # list_options = set(['r', 'q', 't', 'recent', 'questions', 'tags'])
    row_offset = 0
    cmd = s.list_string.split(' ')
    c = s.cursor
    d(print, 'lists recents')
    d(print, f'probably, you wanted to list: {cmd}')
    if len(cmd) > 2:
        d(print, 'Invalid option')
        d(print, switcher_help['ls'])
        return
    how_many = None
    try:
        how_many = cmd[1]
    except:
        how_many = s.how_many  # default show only 10 records?
    # what_to_show = cmd[1]
    d(print, f"omg you want this? : recents, {how_many} items")
    q = f"SELECT question_id, visited_count, last_visited FROM recents ORDER BY last_visited ASC, visited_count DESC  LIMIT {how_many} OFFSET {row_offset}"
    c.execute(q)
    res = c.fetchall()
    # title = 'QuestionID'.ljust(12) + 'Visited'.ljust(12) + 'Time'.ljust(12)
    # print(title)
    headers = ['Question ID', 'Visited', 'Time']
    data = []
    for row in res:
        row = [str(each) for each in row]
        data.append([row[0], row[1], readable_date(row[2])])
    print(prettify_table(data, headers))


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


def add_questions_to_tags():
    print('Add questions to tags')
    print(f'tags: {s.tags}')
    print(f'questions: {s.questions_list}')


# default mode switcher
switcher = {
    '': do_nothing,
    'q': exit_program,
    'h': print_help,
    'ls': list_command,
    'crawler': crawler,
    'debug-toggle': debug_toggle,
    'quit': exit_program,
    'help': print_help,
    'clear': clear_screen,
    'open': open_questions,
    'add_q_to_tags': add_questions_to_tags
}

# help description for each action
switcher_help = {
    'q': "Alias to quit. Exit the program normally.",
    'h': "Alias to help. Shows available commands.",
    '#': "Alias to tags. Lists tags.",
    'tags': "List tags.",
    'open': 'if a number, or multiple comma separated numbers are provided, without any command, each one will be treated as question ID, and will be opened in browser.',
    'ls': "List recently opened links.",
    'quit': "Exit the program normally.",
    'help': "Shows available commands.",
    'clear': "Clear output screen.",
    'debug-toggle': "Toggle debug output.",
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
