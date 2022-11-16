from db import *

RECENT_MESSAGE_COUNT = 20

def get_convLongId(uidList):
    return ':'.join(sorted(uidList))