from xmlrpc import client as xmlrpclib
from urllib.parse import urlsplit


class LAVA(object):
    def __init__(self, url, username, token):
        self.url = url
        self.username = username
        self.token = token
        self.__proxy__ = None

    @property
    def proxy(self):
        if self.__proxy__ is None:
            url = urlsplit(self.url)
            endpoint = '%s://%s:%s@%s%s' % (
                url.scheme,
                self.username,
                self.token,
                url.netloc,
                url.path
            )
            self.__proxy__ = xmlrpclib.ServerProxy(endpoint)
        return self.__proxy__
