import re
import requests

from module.spier import Spier
from module.error import SpierEnd

class Twitter(Spier):
    site = 'twitter'

    api = {
        'followers': 'https://api.twitter.com/1.1/followers/list.json',
        'followings': 'https://api.twitter.com/1.1/friends/ids.json',
        'block': 'https://api.twitter.com/1.1/blocks/create.json'
    }

    params = {
        'count': 10,
        'include_blocking': 1
    }

    def __init__(self, authorization, url, proxy):
        super(Twitter, self).__init__(authorization, proxy)

        re_list = re.match('https://twitter.com/(?P<name>\S+)/(?P<type>\S+)', url).groupdict()
        self._user_name = re_list['name']
        self._user_type = re_list['type']

        self.headers['Authorization'] = authorization
        self.headers['Cookie'] = 'twid=u%3D828521567172718593; ct0=2229e77ae19c41f79caca8c7fbd0ea26; external_referer=JbKFAfGwv4SgAzT2KTilWGgwnT9ATeBH|0|8e8t2xd8A2w%3D; auth_token=654eb2fd10a0627507878b78aff5601179eb51db; kdt=InRyM91rowQjqnkX3Ps1hifQxVIiIvJhKjWUxrsV; remember_checked_on=1; rweb_optin=side_no_out; csrf_same_site=1; csrf_same_site_set=1; ads_prefs="HBIRAAA="; guest_id=v1%3A157685577800632405; personalization_id="v1_W5/TGQaFIE+5URljdRYmPQ=="'
        self.headers['x-twitter-auth-type'] = 'OAuth2Session'
        self.headers['x-csrf-token'] = '2229e77ae19c41f79caca8c7fbd0ea26'
        self.headers['x-twitter-active-user'] = 'yes'

    def get(self, url, params):
        return requests.get(
            url=url,
            headers=self.headers,
            proxies=self.proxies,
            params=params,
            timeout=20,
            verify=False
            )

    next_cursor = -1
    def getUsers(self):
        if self.next_cursor == 0: raise SpierEnd

        params = dict({
                'screen_name': self._user_name,
                'cursor': self.next_cursor
            }, **self.params)
        res = self.get(self.api['followers'], params).json()

        allUsers = list()
        for user in res['users']:
            newUser = {
                    'name': user['screen_name'],
                    'id': user['id_str'],
                    'blocked':  user['blocking'] 
                }
            allUsers.append(newUser)

        self.next_cursor = res['next_cursor']

        return allUsers

    def toBlock(self, user):
        data = {
            'user_id': user['id']
        }
        req = requests.post(self.api['block'], data=data, headers=self.headers, proxies=self.proxies)
        res = req.json()

        data = dict()
        data['name'] = res['name']

        return data