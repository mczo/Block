import sys, inspect, re

from .bilibili import Bilibili
from .twitter import Twitter

def getSpier(args):
    for _, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if re.search(obj.site, args.url, re.I):
            return obj(args.authorization, args.url, args.proxy)