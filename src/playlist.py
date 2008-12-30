#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Playlist(LastfmBase):
    """A class representing an XPSF playlist."""
    def init(self, api, url):
        self.__api = api
        self.__data = None
        self.__url = url

    @LastfmBase.cachedProperty
    def data(self):
        """playlist's data"""
        params = {'method': 'playlist.fetch', 'playlistURL': self.__url}
        tmp = StringIO.StringIO()
        ElementTree.ElementTree(self.__api._fetch_data(params)[0]).write(tmp)
        return tmp.getvalue()
    
    @property
    def url(self):
        """url of the playlist"""
        return self.__url
    
    @staticmethod
    def fetch(api, url):
        return Playlist(api, url = url)
    
    @staticmethod
    def hash_func(*args, **kwds):
        try:
            return hash(kwds['url'])
        except KeyError:
            raise InvalidParametersError("url has to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hash_func(url = self.url)
    
    def __eq__(self, other):
        return self.url == other.url
    
    def __lt__(self, other):
        return self.url < other.url
    
    def __repr__(self):
        return "<lastfm.Playlist: %s>" % self.url

import StringIO
import platform
from error import InvalidParametersError

python_version = platform.python_version_tuple()
if python_version[0] == 2 and python_version[1] >= 5:
    import xml.etree.cElementTree as ElementTree
else:
    try:
        import cElementTree as ElementTree
    except ImportError:
        try:
            import ElementTree
        except ImportError:
            from error import Error
            raise Error("Install ElementTree package for using python-lastfm")