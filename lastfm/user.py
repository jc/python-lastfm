#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class User(LastfmBase):
    """A class representing an user."""
    def __init__(self,
                 api,
                 name = None,
                 url = None,
                 image = None):
        self.__api = api
        self.__name = name
        self.__url = url
        self.__image = image

    def getName(self):
        return self.__name

    def getUrl(self):
        return self.__url

    def getImage(self):
        return self.__image

    name = property(getName, None, None, "Name's Docstring")

    url = property(getUrl, None, None, "Url's Docstring")

    image = property(getImage, None, None, "Image's Docstring")
    
    def getEvents(self):
        pass
    
    events = property(getEvents, None, None, "docstring")
    
    def getFriends(self,
                   recentTracks = False,
                   limit = None):
        pass
    
    friends = property(getFriends, None, None, "docstring")
    
    def getNeighbours(self, limit = None):
        pass
    
    neighbours = property(getNeighbours, None, None, "docstring")
    
    def getPlaylists(self):
        pass
    
    playlists = property(getPlaylists, None, None, "docstring")
    
    def getRecentTracks(self, limit = None):
        pass
    
    recentTracks = property(getRecentTracks, None, None, "docstring")
    
    def getTopAlbums(self, period = None):
        pass
    
    topAlbums = property(getTopAlbums, None, None, "docstring")
    topAlbum = property(lambda self: len(self.topAlbums) and self.topAlbums[0],
                   None, None, "docstring")
    
    def getTopArtists(self, period = None):
        pass
    
    topArtists = property(getTopArtists, None, None, "docstring")
    topArtist = property(lambda self: len(self.topArtists) and self.topArtists[0],
                   None, None, "docstring")
    
    def getTopTracks(self, period = None):
        pass
    
    topTracks = property(getTopTracks, None, None, "docstring")
    topTrack = property(lambda self: len(self.topTracks) and self.topTracks[0],
                   None, None, "docstring")
    
    def getTopTags(self, limit = None):
        pass
    
    topTags = property(getTopTags, None, None, "docstring")
    topTag = property(lambda self: len(self.topTags) and self.topTags[0],
                   None, None, "docstring")
    
    def getWeeklyChartList(self):
        pass

    def getWeeklyAlbumChart(self,
                             start = None,
                             end = None):
        pass
    
    weeklyAlbumChart = property(getWeeklyAlbumChart, None, None, "Docstring")
    
    def getWeeklyArtistChart(self,
                             start = None,
                             end = None):
        pass
    
    weeklyArtistChart = property(getWeeklyArtistChart, None, None, "Docstring")
    
    def getWeeklyTrackChart(self,
                             start = None,
                             end = None):
        pass
    
    weeklyTrackChart = property(getWeeklyTrackChart, None, None, "Docstring")
    
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
        return "<lastfm.User: %s>" % self.name