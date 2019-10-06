import re
import requests

from module.spier import Spier

class Bilibili(Spier):
    api = {
        'followers': 'https://api.bilibili.com/x/relation/followers',
        'followings': 'https://api.bilibili.com/x/relation/followings',
        'block': 'https://api.bilibili.com/x/relation/modify'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
    }
    params = {
        'order': 'desc',
        'jsonp': 'jsonp'
    }

    def __init__(self, authorization, url, proxy):
        super(Bilibili, self).__init__(proxy)
        
        for cookieItem in authorization.split('; '):
            [key, value] = re.split('=', cookieItem)
            self._cookie[key.strip()] = value.strip()
        self.headers['Cookie'] = authorization

        self._userid = re.findall(r'\d+', url)[0]
        # self._userid = self.getUserId(self.userName)
        # print(self._userid)
        

    def get(self, url, params):
        return requests.get(
            url=url,
            headers=self.headers,
            proxies=self.proxies,
            params=params,
            timeout=10,
            verify=False
            )

    def getUsers(self, count=50):
        self.page += 1
        params = dict({
            'vmid': self._userid,
            'pn': self.page,
            'ps': count,
        }, **self.params)

        res = self.get(self.api['followers'], params).json()

        allUsers = list()
        for user in res['data']['list']:
            if user['attribute']:
                user['blocked'] = True
            allUsers.append(user)
            
        return (allUsers, res['data']['total'])

    def toBlock(self, user):
        data = {
            'fid': user['mid'],
            'act': '5',
            're_src': '11',
            'jsonp': 'jsonp',
            'csrf': self._cookie['bili_jct']
        }

        req = requests.post(self.api['block'], data=data, headers=self.headers)
        res = req.json()

        print(res)
        