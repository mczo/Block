import re
import requests

from module.spier import Spier
from module.error import SpierEnd


class Bilibili(Spier):
    site = 'bilibili'
    
    api = {
        'followers': 'https://api.bilibili.com/x/relation/followers',
        'followings': 'https://api.bilibili.com/x/relation/followings',
        'block': 'https://api.bilibili.com/x/relation/modify'
    }
    params = {
        'order': 'desc',
        'jsonp': 'jsonp'
    }

    queueUsers = set()
    endUsers = set()

    def __init__(self, authorization, url, proxy):
        super(Bilibili, self).__init__(authorization, proxy)
        
        self._cookie = dict( map( lambda i: i.strip().split('='), authorization.split(';') ) )
        self.headers['Cookie'] = authorization

        self._userid = int( re.findall(r'\d+', url)[0] )
        self.queueUsers.add(self._userid)

    def get(self, url, params):
        return requests.get(
            url=url,
            headers=self.headers,
            proxies=self.proxies,
            params=params,
            timeout=10,
            verify=False
            )

    def getFollowers(self, userid):
        page = 1
        allUsers = list()

        while(page <= 5):
            params = dict({
                'vmid': userid,
                'pn': page,
                'ps': 50,
            }, **self.params)
            res = self.get(self.api['followers'], params).json()

            for user in res['data']['list']:
                self.queueUsers.add(user['mid'])
                newUser = {
                    'name': user['uname'],
                    'id': user['mid'],
                    'blocked': True if user['attribute'] else False 
                }
                allUsers.append(newUser)

            page += 1

        return allUsers

    def getUsers(self):
        currentUserId = self.queueUsers.pop()

        if currentUserId in self.endUsers:
            return self.getUsers()

        self.endUsers.add(currentUserId)
        return self.getFollowers(currentUserId)

    def toBlock(self, user):
        data = {
            'fid': user['id'],
            'act': '5',
            're_src': '11',
            'jsonp': 'jsonp',
            'csrf': self._cookie['bili_jct']
        }

        req = requests.post(self.api['block'], data=data, headers=self.headers)
        res = req.json()

        if not res['code']:
            return True
            
        return False
        