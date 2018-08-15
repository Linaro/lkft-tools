import netrc

from urllib.parse import urlsplit


class Auth(object):
    def __init__(self, url):
        self.url = urlsplit(url).netloc
        netrcauth = netrc.netrc()
        self.username, _, self.token = netrcauth.authenticators(self.url)
