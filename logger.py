import logging
import sys
from constants import DEBUG
# for later
# logging.basicConfig(filename="debug_log.txt", level=logging.DEBUG)
# d = logging.debug
# i = logging.info


def d(f, args):
    if DEBUG == True:
        print('DEBUG: ', end="")
        f(args)
    else:
        return
