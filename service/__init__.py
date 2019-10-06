import sys, inspect, re

from .twitter import Twitter
from .bilibili import Bilibili

def getSpier(args):
    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if re.search(name, args.url, re.I):
            return obj(args.authorization, args.url, args.proxy)