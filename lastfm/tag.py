#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Tag(object):
    """"A class representing a tag."""
    def __init__(self,
                 api,
                 name = None,
                 url = None):
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
    
from album import Album
from artist import Artist
from track import Track