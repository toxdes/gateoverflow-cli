# project name
project_name = "gateoverflow"
database_name = "gateoverflow.db"
title_text = 'G a t e O v e r f l o w'

# TODO: what if unicodes are not supported in terminal ?
shell_symbol = "→ "


class modes():
    DEFAULT = 'default',


class parser_actions:
    LIST_QUESTIONS_OF_TAGS = 1,
    OPEN_QUESTIONS = 2,
    LIST_TAGS = 3,
    ADD_QUESTIONS_TO_TAGS = 4


metadata_api_base = "http://url-metadata.herokuapp.com"

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


class User:
    def __init__(self, username='anonymous_user', name='bruh'):
        self.username = username
        self.name = name

    def greet(self):
        return f'Welcome, @{self.username}'


sample_config = '''
# database filename
database_name="gateoverflow.db"

# shell symbol to show
shell_symbol ="→ "

# for ls command, how many records to show by default
how_many=10
title_text="G a t e O v e r f l o w"

# crawl_attempts_limit in order to delete possibly invalid question ids
crawl_attempts_limit = 5

# column_width: number of characters to allow for each column
# if the data has more characters than this limit, it is truncated with adding "..." in the end
# for example, "bruhbruhbruhbruh" will turn into "bruh..." if column width is 7
# should be at least 10 cause the timestamp thing
column_width = 12
'''
