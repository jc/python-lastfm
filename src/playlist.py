#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Playlist(LastfmBase):
    """A class representing an XPSF playlist."""
    def init(self, xpsfData, url):
        self.__data = xpsfData
        self.__url = url

    @property
    def data(self):
        """playlist's data"""
        return self.__data
    
    @property
    def url(self):
        """url of the playlist"""
        return self.__url
    
    @staticmethod
    def fetch(api, url):
        params = {'method': 'playlist.fetch', 'playlistURL': url}
        return Playlist(api._fetchData(params, parse = False), url = url)
    
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['url'])
        except KeyError:
            raise LastfmInvalidParametersError("url has to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(url = self.url)
    
    def __eq__(self, other):
        return self.url == other.url
    
    def __lt__(self, other):
        return self.url < other.url
    
    def __repr__(self):
        return "<lastfm.Playlist: %s>" % self.url
    
from error import LastfmInvalidParametersError