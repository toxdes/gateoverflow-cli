import state as s


def exit_program():
    s.stop = True


def print_help():
    print("Commands - ")
    for each in switcher.keys():
        try:
            print(f'\t{each}\t-\t{ switcher_help[each]}')
        except:
            print(f"Help not available for command: {each}")


# actions switcher
# TODO: Find a better way to structure this
switcher = {
    'q': exit_program,
    'quit': exit_program,
    'h': print_help,
    'help': print_help,
}

# help description for each action
switcher_help = {
    'q': "Alias to quit. Exit the program normally.",
    'quit': "Exit the program normally.",
    'h': "Alias to help. Shows available commands.",
    'help': "Shows available commands.",
}
