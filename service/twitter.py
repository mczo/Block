import re
import requests

from module.spier import Spier
from module.error import SpierEnd

class Twitter():
    site = 'twitter'

    def __init__(self, authorization, url, proxy):
        super(Twitter, self).__init__(authorization, proxy)

        # self._userid = int( re.findall(r'\d+', url)[0] )
        # self.queueUsers.add(self._userid)