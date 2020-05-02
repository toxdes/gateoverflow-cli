import os
from gateoverflow import state as s
from gateoverflow import constants
from gateoverflow.logger import d
from gateoverflow import queries as q
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
    c.execute(q.get_recent, (how_many, row_offset))
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


def invalid_command():
    print("Invalid command, h to show available commands.")


class Parser:
    @staticmethod
    def list_tags():
        c = s.cursor
        res = c.execute(q.get_tags)
        print(f'List of tags...')
        if res == None:
            print("No tags are created yet :(")
        for each in res:
            print(f'#{each[0]} ({each[1]} questions)')

    @staticmethod
    def open_questions():
        print('Number(s) found, treating them as questionIDs, and opening each in web-browser...')
        # get the input list, stored in state
        question_ids = s.questions_list
        # insert into recent questions table, along with timestamp, update visited count if already visited
        c = s.cursor
        for each in question_ids:
            # check if already exists
            c.execute(q.get_question, [each])
            res = c.fetchone()
            if res != None:
                # update
                c.execute(q.update_visited_count, [
                    each, each])
            else:
                # insert
                c.execute(q.insert_into_recents, [each])
            open_link(f'https://gateoverflow.in/{each}')
        s.conn.commit()
        print('Done!')

    @staticmethod
    def list_questions_of_tags():
        print(f'Only tag(s) found, listing questions of specified tags...')
        tags, questions = s.tags, s.questions_list
        c = s.cursor
        res = c.execute(q.get_tags)
        tags_in_db = []
        for each in res:
            tags_in_db.append(each[0])
        non_existant_tags = []
        existant_tags = []
        tags = [a[1:] for a in tags]
        for each in tags:
            if each not in tags_in_db:
                d(print, f'Tag {each} does not exist.')
                non_existant_tags.append(each)
                continue
            existant_tags.append(each)
        d(print, f'Existant tags: {existant_tags}')
        if len(existant_tags) != 0:
            # TODO: find a way to move this query to queries.py
            query = f'SELECT question_id, (select name from tags where id=tag_id) from tq_relation as TQ WHERE tag_id IN (SELECT id FROM tags WHERE name IN ({"?"*len(existant_tags)}))'
            res = c.execute(query, existant_tags)
            if res == None:
                print('Nothing to show.')
                return
            for each in res:
                d(print, f'Question:{each[0]}\t Tag: #{each[1]}')

    @staticmethod
    def add_questions_to_tags():
        print(f'Adding {s.questions_list} to {s.tags}...')
        tags, questions = s.tags, s.questions_list
        c = s.cursor
        res = c.execute(q.get_tags)
        tags_in_db = []
        for each in res:
            tags_in_db.append(each[0])
        non_existant_tags = []
        existant_tags = []
        tags = [a[1:] for a in tags]
        create_tags_script = ''
        for each in non_existant_tags:
            ans = input(
                f'Tag #{each} does not exist, do you want to create it?(y/n)')
            ans = ans.tolower()
            if(ans == 'y' or ans == 'yes'):
                create_tags_script = f'{create_tags_script}\nINSERT INTO tags(name,questions_count) VALUES ({each},0);'
        c.executescript(create_tags_script)
        s.conn.commit()
        tq_insert_script = ''
        for q_id in questions:
            for tag in tags:
                tq_insert_script = f'{tq_insert_script}\nINSERT OR REPLACE INTO tq_relation(question_id,tag_id) VALUES ({q_id},(SELECT id FROM tags WHERE name=\'{tag}\'));'
        c.executescript(tq_insert_script)
        s.conn.commit()


def handle_parser_action():
    pa = constants.parser_actions
    if s.parser_action == pa.LIST_TAGS:
        Parser.list_tags()
        return
    if s.parser_action == pa.OPEN_QUESTIONS:
        Parser.open_questions()
        return
    if s.parser_action == pa.LIST_QUESTIONS_OF_TAGS:
        Parser.list_questions_of_tags()
        return
    if s.parser_action == pa.ADD_QUESTIONS_TO_TAGS:
        Parser.add_questions_to_tags()
        return
    invalid_command()


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
    'parser': handle_parser_action,
    'invalid': invalid_command,
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
