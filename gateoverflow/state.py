# global variables
# controls polling, setting to true exits the program
from gateoverflow import constants
from gateoverflow.helpers import prettify_table
stop = False
mode = constants.modes.DEFAULT
switcher = None
# questions_list = [22, 23, 12, 232, 2]
questions_list = []
tags = []
cursor = None

# when listing things, how many records to show, defaults to 10
how_many = 10

# list command
list_string = 'ls'

# debug output
DEBUG = False

# title
title_text = prettify_table([['G a t e   o v e r f l o w'.upper()]], [])
