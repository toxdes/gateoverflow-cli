import sys
import logging
from gateoverflow.state import state as s
from gateoverflow import constants
# for later
# logging.basicConfig(filename="debug_log.txt", level=logging.DEBUG)
# d = logging.debug
# i = logging.info


# TODO: Write all debug output to a debug file

def d(f, args):
    if s['DEBUG'] == True:
        if(f == 't'):
            print(
                f'{constants.colors.GREEN}REACHED TARGET:{constants.colors.END} {args}')
        else:
            print(f'{constants.colors.WARNING}DEBUG:{constants.colors.END} ', end="")
            f(args)
    else:
        return
