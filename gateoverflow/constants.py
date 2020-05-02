database_name = "test_database.db"
title_text = '''
********************
* GO LINKS MANAGER *
********************
'''

# TODO: what if unicodes are not supported in terminal ?
shell_symbol = "→ "


class modes():
    DEFAULT = 'default',


class parser_actions:
    LIST_QUESTIONS_OF_TAGS = 1,
    OPEN_QUESTIONS = 2,
    LIST_TAGS = 3,
    ADD_QUESTIONS_TO_TAGS = 4


metadata_api_base = "http =//url-metadata.herokuapp.com"

# colored text


class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
