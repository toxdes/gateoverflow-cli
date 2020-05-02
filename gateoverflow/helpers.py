from datetime import datetime
import shlex
from tabulate import tabulate
import os
import subprocess
from pprint import pprint
from dateutil.relativedelta import relativedelta
import requests
import json
from gateoverflow.logger import d
from gateoverflow import constants
from gateoverflow import state as s

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


def list_of_ints(in_str):
    error = False
    nums = []
    try:
        nums = [int(a) for a in in_str.split(',')]
    except:
        error = True
    return (error, nums)

# checks if string is list of comma seperated ints and includes tags
# for example 23,42,12, #important, #wrong -> valid


def list_of_ints_and_tags(in_str):
    error = False
    nums = []
    tags = []
    line = [a.strip() for a in in_str.split(',')]
    print(line)
    for each in line:
        try:
            int(each)
            nums.append(each)
        except:
            if(each[0] == '#'):
                if(len(each.split(' ')) > 1):
                    [tags.append(a) for a in each.split(' ')]
                else:
                    tags.append(each)
            else:
                error = True
                break
    return (error, nums, tags)
# open each link in the browser, this should be cross platform


def open_link(link):
    # TODO: Figure out a way to suppress terminal output of browser
    # google-chrome output is shown on the terminal
    d(print, f'opening {link} in browser')
    try:
        # webbrowser.get().open(link)
        subprocess.run(shlex.split(
            f'xdg-open {link}'), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        # we're on termux / there's no native browser available
        # there's an alternative to this
        # ask user to set $BROWSER='termux-open-url' / or do it during install?
        subprocess.run(
            shlex.split(f'termux-open-url {link}'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# crawl metadata information, will be useful later


def uncrawled_metadata_count():
    query = "SELECT COUNT(*) FROM recents WHERE metadata_scraped=0"
    c = s.cursor
    c.execute(query)
    res = c.fetchone()
    d(print, f'Unscraped Records: {res[0]}')
    return int(res[0])


def crawl_metadata():
    query = "SELECT question_id FROM recents WHERE metadata_scraped=0"
    c = s.cursor
    c.execute(query)
    res = c.fetchall()
    stmt = ""
    for each in res:
        each = int(each[0])
        data = get_metadata(f'https://gateoverflow.in/{each}')
        if data == None:
            continue
        q = 'INSERT OR REPLACE INTO metadata(question_id, title, desc, image_url) values(?,?,?,?)'
        c.execute(q, (each, data['title'],
                      data['desc'], data['image_url']))
        c.execute(
            f'UPDATE recents SET metadata_scraped=1 WHERE question_id={each}')


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
        res['title'] = data['title']
    except:
        print('maybe internet is down. Error, Skipping!')
        res = None
    return res

# pretty tables


def prettify_table(data, headers):
    return str(tabulate(data, headers=headers, tablefmt='fancy_grid',
                        numalign='center', stralign='center'))


def print_logo():
    print(f'{constants.colors.GREEN}{constants.colors.BOLD}{s.title_text}{constants.colors.END}{constants.colors.END}')
