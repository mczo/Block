class Spier(object):
    site = ''

    proxies = {
        'http': 'socks5://',
        'https': 'socks5://'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
    }
    
    _authorization = ''
    _userid = ''
    _cookie = {}
    api = {}

    def __init__(self, authorization, proxy):
        if not proxy:
            self.proxies = {}
        else:
            self.proxies = dict( zip( self.proxies, map( lambda v: v + proxy, self.proxies.values() ) ) )