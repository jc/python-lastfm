#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Playlist(LastfmBase):
    """A class representing an XPSF playlist."""
    def init(self, xpsfData, url):
        self.__data = xpsfData
        self.__url = url

    def getData(self):
        return self.__data
    
    def getUrl(self):
        return self.__url
    
    data = property(getData, None, None, "docstring")

    url = property(getUrl, None, None, "url's Docstring")
        
    @staticmethod
    def fetch(api, url):
        params = {'method': 'playlist.fetch', 'playlistURL': url}
        return Playlist(api.fetchData(params, parse = False), url = url)
    
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['url'])
        except KeyError:
            raise LastfmError("url has to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(url = self.url)
    
    def __eq__(self, other):
        return self.url == other.url
    
    def __lt__(self, other):
        return self.url < other.url
    
    def __repr__(self):
        return "<lastfm.Playlist: %s>" % self.url
    
from error import LastfmError