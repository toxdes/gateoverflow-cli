import os
from pprint import pprint
import webbrowser
import state as s
import constants
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


def debug_state():
    print(f'mode:{s.mode}')
    print(f'stop: {s.stop}')


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
        # open each link in the browser, this should be cross platform
        # TODO: Figure out a way to suppress terminal output of browser
        # google-chrome output is shown on the terminal for me
        webbrowser.get().open(f'https://gateoverflow.in/{each}')


# default mode switcher
switcher = {
    '': do_nothing,
    'q': exit_program,
    'h': print_help,
    'o': open_mode,
    'debug-state': debug_state,
    'quit': exit_program,
    'help': print_help,
    'clear': clear_screen,
    'open-mode': open_mode,
    'open': open_questions
}

open_mode_switcher = {
    '': do_nothing,
    'q': exit_program,
    'h': print_help,
    'quit': exit_program,
    'help': print_help,
    'open': open_questions
}
# help description for each action
switcher_help = {
    'q': "Alias to quit. Exit the program normally.",
    'h': "Alias to help. Shows available commands.",
    'o': "Alias to open-mode. Go into open-mode.",
    'quit': "Exit the program normally.",
    'help': "Shows available commands.",
    'clear': "Clear output screen.",
    'open-mode': "Go into open-mode",
    'open': 'if a number, or multiple comma separated numbers are provided, without any command, each one will be treated as question ID, and will be opened in browser.'
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
