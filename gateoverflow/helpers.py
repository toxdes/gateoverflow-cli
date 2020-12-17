from datetime import datetime
import shlex
from tabulate import tabulate
import os
import subprocess
import sys
import re
import webbrowser
from pprint import pprint
from dateutil.relativedelta import relativedelta
import requests
import json
from gateoverflow.logger import d
from gateoverflow import constants
from gateoverflow.state import state as s
from gateoverflow import actions as a
from gateoverflow import queries as q
from gateoverflow import __version__
# TODO: oh poor me, please update this function later for avoiding embarrassement


def readable_date(date):
    delta = relativedelta(datetime.now(), datetime.fromtimestamp(int(date)))
    res = ''
    d(pprint, delta)
    order = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
    delta = [delta.years, delta.months, delta.days,
             delta.hours, delta.minutes, delta.seconds]
    i = 0
    while i < len(delta):
        if delta[i] == 0:
            i += 1
        else:
            break
    if(i >= len(delta)):
        res = "Just Now"
    else:
        res = f'{delta[i]} {order[i]} ago'
    return res

# checks if string is list of comma seperated integers only


# def list_of_ints(in_str):
#     error = False
#     nums = []
#     try:
#         nums = [int(a) for a in in_str.split(',')]
#     except:
#         error = True
#     error = True
#     return (error, nums)

# checks if string is list of comma seperated ints and includes tags
# for example 23,42,12, #important, #wrong -> valid


def parse_cmd(in_str):
    error = False
    nums = []
    tags = []
    action = None
    if(in_str == 'tags' or in_str == '#'):
        action = constants.parser_actions.LIST_TAGS
        return (error, nums, tags, action)
    line = [a.strip() for a in in_str.split(',')]
    d(print, line)
    for each in line:
        try:
            if(len(each.split(' ')) > 1):
                [nums.append(int(a)) for a in each.split(' ')]
            else:
                nums.append(int(each))
        except:
            # fixes trailing commas and inputs like `,,,` `#,#,#`
            if(len(each) < 1 or each == '#'):
                continue
            # if multiple #'s are there, then it should be invalid
            if(each[0] == '#' and each.count('#') == 1):
                if(len(each.split(' ')) > 1):
                    [tags.append(a) for a in each.split(' ')]
                else:
                    tags.append(each)
            else:
                error = True
                break
    if error:
        return (error, nums, tags, action)
    if(len(nums) == 0):
        action = constants.parser_actions.LIST_QUESTIONS_OF_TAGS
    if(len(tags) == 0):
        action = constants.parser_actions.OPEN_QUESTIONS
    if(len(tags) == 0 and len(nums) == 0):
        action = constants.parser_actions.DO_NOTHING
    d(print, f'error: {error}')
    d(print, f'nums: {nums}')
    d(print, f'tags: {tags}')
    if action == None:
        action = constants.parser_actions.ADD_QUESTIONS_TO_TAGS
    return (error, nums, tags, action)
# open each link in the browser, this should be cross platform


def open_link(link):
    # TODO: Figure out a way to suppress terminal output of browser
    # google-chrome output is shown on the terminal
    d(print, f'opening {link} in browser')
    try:
        webbrowser.get().open(link)
        # subprocess.run(shlex.split(
        #     f'xdg-open {link}'), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        # we're on termux or android and there's no native browser available
        # there's an alternative to this
        # ask user to set $BROWSER='termux-open-url' / or do it during install?
        try:
            subprocess.run(
                shlex.split(f'termux-open-url {link}'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            print("No browser found. Sorry.")

# crawl metadata information, will be useful later


def uncrawled_metadata_count():
    c = s['cursor']
    c.execute(q.uncrawled_metadata_count)
    res = c.fetchone()
    d(print, f'Unscraped Records: {res[0]}')
    return int(res[0])


def crawl_metadata():
    c = s['cursor']
    c.execute(q.get_unscraped_question_ids)
    res = c.fetchall()
    stmt = ""
    for each in res:
        each = int(each[0])
        data = get_metadata(f'https://gateoverflow.in/{each}')
        d(print, f'{data}')
        d(print, f'questionid: {each}')
        c.execute(q.update_crawl_attempts, [each])
        if data == None:
            continue
        c.execute(q.insert_into_metadata, (each, data['title'],
                                           data['desc'], data['image_url']))
        c.execute(
            q.update_metadata_scraped_questions, [each])
    c.execute(q.delete_invalid_questions, [s['crawl_attempts_limit']])


'''
get_metadata(link) returns a dictionary Data
Data{title, desc, image_url} or None on Failure
'''


def get_metadata(link):
    print(f'crawling meta information for site: {link}')
    res = None
    try:
        r = requests.get(
            f'{constants.metadata_api_base}/api/metadata?url={link}')
        data = json.loads(r.text)
        data = data['data']
        res = {}
        res['title'] = data['title']
        res['desc'] = data['description']
        res['image_url'] = data['image']
    except Exception as e:
        print(
            'Maybe internet is down, or question_id is invalid, or other Error, Skipping!')
        d(print, f'Error: {e}')
        res = None
    return res

# pretty tables


def prettify_table(data, headers):
    return str(tabulate(data, headers=headers, tablefmt='fancy_grid',
                        numalign='center', stralign='center'))


def print_title():
    print(
        f'{constants.colors.GREEN}{constants.colors.BOLD}{prettify_table([[s["title_text"].upper()]], [])}{constants.colors.END}{constants.colors.END}')
    print(s['user'].greet())


def ask():
    q = input("Proceed? (y/n) (default: n): ")
    return q.lower() == 'yes' or q.lower() == 'y'


def askPositive():
    q = input("Proceed? (y/n) (default: y): ")
    return q.lower() != 'no' and q.lower() != 'n'

# sends HTTP request to pypi and pattern matches with version string.


def latest_version_check():
    print('Checking for latest update...')
    res = None
    try:
        res = requests.get('https://pypi.org/project/gateoverflow')
        if not res.ok:
            d('t', "Request to pypi website failed, result of GET is not OK")
            print("Request to server failed.")
            return
        res = str(res.text)
    except:
        print("Couldn't connect to the Internet.")
        return

    p = re.compile("gateoverflow \d\.\d\.\d")
    matches = [str(each) for each in p.findall(res)]
    if len(matches) < 1:
        return
    matches = [matches[0][len('gateoverflow '):]]
    matches.append(__version__)
    d(print, f'Matches are: {matches}')
    if matches[0] != matches[1]:
        one = [int(each) for each in matches[0].split('.')]
        two = [int(each) for each in matches[1].split('.')]
        print(f'Latest release: {matches[0]}')
        for i in range(len(one)):
            if(one[i] == two[i]):
                continue
            if(two[i] > one[i]):
                print('You are ahead of the lastest stable release.\nNice!')
                return
            print(
                f'You are not using the latest release. To upgrade to a latest release, run ')
            print(prettify_table(
                [['python -m pip install gateoverflow --upgrade']], []))
            break
    else:
        print('You are already at a latest release.')
    pass


# reads default_config.toml file and returns string of it
def get_default_config():
    f = None
    try:
        f = open(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "default_config.toml"), 'r')
    except:
        d(print, f"Error: Cannot open default_config.toml, something's wrong with packaging.")
    if f == None:
        a.abort_program()
    res = ''
    for line in f.readlines():
        res = f'{res}{line}'
    f.close()
    return res
