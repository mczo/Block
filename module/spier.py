class Spier(object):
    proxies = {
        'http': 'socks5://',
        'https': 'socks5://'
    }
    
    _authorization = ''
    _userid = ''
    _cookie = {}

    page = 0

    def __init__(self, proxy):
        if not proxy:
            self.proxies = {}