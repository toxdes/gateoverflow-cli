# global variables
# controls polling, setting to true exits the program
import constants
stop = False
mode = constants.modes.DEFAULT
switcher = None
# questions_list = [22, 23, 12, 232, 2]
questions_list = []
cursor = None

# when listing things, how many records to show, defaults to 10
how_many = 10

# list command
list_string = 'ls recent'

# debug output
DEBUG = False
