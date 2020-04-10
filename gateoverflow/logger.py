import sys
import logging
from gateoverflow import state as s
# for later
# logging.basicConfig(filename="debug_log.txt", level=logging.DEBUG)
# d = logging.debug
# i = logging.info


def d(f, args):
    if s.DEBUG == True:
        print('DEBUG: ', end="")
        f(args)
    else:
        return
