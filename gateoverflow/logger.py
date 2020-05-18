import sys
import logging
from gateoverflow.state import state as s
# for later
# logging.basicConfig(filename="debug_log.txt", level=logging.DEBUG)
# d = logging.debug
# i = logging.info


def d(f, args):
    if s['DEBUG'] == True:
        if(f == 't'):
            print(f'Reached TARGET: {args}')
        else:
            print('DEBUG: ', end="")
            f(args)
    else:
        return
