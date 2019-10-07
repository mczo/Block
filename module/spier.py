class Spier(object):
    proxies = {
        'http': 'socks5://',
        'https': 'socks5://'
    }
    
    _authorization = ''
    _userid = ''
    _cookie = {}

    def __init__(self, proxy):
        if not proxy:
            self.proxies = {}