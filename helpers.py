from datetime import datetime
import os
import webbrowser
import subprocess
from pprint import pprint
from dateutil.relativedelta import relativedelta
import requests
import json
from logger import d
import constants
import state as s

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

# open each link in the browser, this should be cross platform


def open_link(link):
    # TODO: Figure out a way to suppress terminal output of browser
    # google-chrome output is shown on the terminal
    d(print, f'opening {link} in browser')
    try:
        webbrowser.get().open(f'https://gateoverflow.in/{link}')
    except:
        # we're on termux / there's no native browser available
        # there's an alternative to this
        # ask user to set $BROWSER='termux-open-url' / or do it during install?
        subprocess.run(
            f'termux-open-url {link}', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# crawl metadata information


def crawl_for_metadata():
    query = "SELECT COUNT(*) FROM recents WHERE metadata_scraped=0"
    c = s.cursor
    c.execute(query)
    res = c.fetchone()[0]
    print(f"Unscraped Records: {res}")
    # data = get_metadata('https://gateoverflow.in/3453')


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
        res['image_url'] = data['image_url']
        res['title'] = data['title']
    except:
        print('maybe internet is down. Error, Skipping!')
        res = None
    return res
