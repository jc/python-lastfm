#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Tag(LastfmBase):
    """"A class representing a tag."""
    def init(self,
                 api,
                 name = None,
                 url = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__url = url
    
    def getName(self):
        return self.__name

    def getUrl(self):
        return self.__url
    
    name = property(getName, None, None, "Name's Docstring")

    url = property(getUrl, None, None, "Url's Docstring")        
    
    def getSimilar(self):
        pass
    
    def getTopAlbums(self):
        pass
    
    def getTopArtists(self):
        pass
    
    def getTopTracks(self):
        pass
    
    @staticmethod
    def getTopTags(api):
        pass
    
    @staticmethod
    def search(api,
               tag,
               limit = None,
               page = None):
        pass
    
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['name'])
        except KeyError:
            raise LastfmError("name has to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(name = self.name)
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __repr__(self):
        return "<lastfm.Tag: %s>" % self.name

from api import Api
from error import LastfmError
from album import Album
from artist import Artist
from track import Track