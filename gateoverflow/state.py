# global variables
from gateoverflow import constants
# from gateoverflow.helpers import prettify_table


state = {
    'stop': False,
    'mode': constants.modes.DEFAULT,
    'switcher': None,
    'questions_list': [],
    'tags': [],
    'parser_action': None,
    'cursor': None,
    'conn': None,
    # when listing things, how many records to show, defaults to 10
    'how_many': 10,

    # list command
    'list_string': 'ls',

    # debug output
    'DEBUG': False,

    # title
    'title_text': constants.title_text,

    # crawl_attempts_limit in order to delete possibly invalid question ids
    'crawl_attempts_limit': 5,

    # 'column_width': number of characters to allow for each column
    # if the data has more characters than this limit, it is truncated with adding "..." in the end
    # for example, "bruhbruhbruhbruh" will turn into "bruh..." if column width is 7
    # should be at least 10 cause the timestamp thing
    'column_width': 12,

    # project root diretory
    'project_home': None,

    # show or hide the title text (the box)
    'show_title': True,
    'shell_symbol': "→ ",
    'database_name': "gateoverflow.db",
    'db_path': None,
    'user': constants.User(),

    # show countdown or not?
    'show_eta_countdown': False,

    # ETA - Deadline/ Exam Date (for showing remaining days until that particular date)
    # date format is dd-mm-yyyy
    'eta_date': '13-02-2020',
    # details about the ETA task you've been wanting to create
    'eta_note': 'no note saved. You may want to check config file.'
}
