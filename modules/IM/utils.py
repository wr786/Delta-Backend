from db import *

def get_convLongId(uidList):
    return ':'.join(sorted(uidList))