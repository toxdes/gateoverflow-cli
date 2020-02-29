import os
import state as s
import constants


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
    print(constants.title_text)
# actions switcher
# TODO: Find a better way to structure this


switcher = {
    'q': exit_program,
    'h': print_help,
    'quit': exit_program,
    'help': print_help,
    'clear': clear_screen
}

# help description for each action
switcher_help = {
    'q': "Alias to quit. Exit the program normally.",
    'h': "Alias to help. Shows available commands.",
    'quit': "Exit the program normally.",
    'help': "Shows available commands.",
    'clear': "Clear output screen."
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
