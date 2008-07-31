#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class User(LastfmBase):
    """A class representing an user."""
    def init(self,
                 api,
                 name = None,
                 url = None,
                 image = None,
                 stats = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__url = url
        self.__image = image
        self.__stats = stats and Stats(
                             subject = self,
                             match = stats.match,
                             weight = stats.weight
                            )

    @property
    def name(self):
        """name of the user"""
        return self.__name

    @property
    def url(self):
        """url of the user's page"""
        return self.__url

    @property
    def image(self):
        """image of the user"""
        return self.__image

    @property
    def stats(self):
        """stats for the user"""
        return self.__stats
        
    @property
    def events(self):
        pass
    
    def getFriends(self,
                   recentTracks = False,
                   limit = None):
        pass
    
    @property
    def friends(self):
        """friends of the user"""
        return self.getFriends()
    
    def getNeighbours(self, limit = None):
        pass
    
    @property
    def neighbours(self):
        """neightbours of the user"""
        return self.getNeighbours()
    
    @property
    def playlists(self):
        """playlists of the user"""
        pass
    
    def getRecentTracks(self, limit = None):
        pass
    
    @property
    def recentTracks(self):
        """recent tracks played by the user"""
        return self.getRecentTracks()
    
    @property
    def mostRecentTrack(self):
        """most recent track played by the user"""
        return (len(self.recentTracks) and self.recentTracks[0] or None)
    
    def getTopAlbums(self, period = None):
        pass
    
    @property
    def topAlbums(self):
        """top albums of the user"""
        return self.getTopAlbums()
    
    @property
    def topAlbum(self):
        """top album fo the user"""
        return (len(self.topAlbums) and self.topAlbums[0] or None)
    
    def getTopArtists(self, period = None):
        pass
    
    @property
    def topArtists(self):
        """top artists of the user"""
        return self.getTopArtists()
    
    @property
    def topArtist(self):
        """top artist of the user"""
        return (len(self.topArtists) and self.topArtists[0] or None)
    
    def getTopTracks(self, period = None):
        pass
    
    @property
    def topTracks(self):
        """top tracks of the user"""
        return self.getTopTracks()
     
    @property
    def topTrack(self):
        """top track of the user"""
        return (len(self.topTracks) and self.topTracks[0] or None)
    
    def getTopTags(self, limit = None):
        pass
    
    @property
    def topTags(self):
        """top tags of the user"""
        return self.getTopTags()
    
    @property
    def topTag(self):
        """top tag of the user"""
        return (len(self.topTags) and self.topTags[0] or None)
    
    @property
    def weeklyChartList(self):
        pass

    def getWeeklyAlbumChart(self,
                             start = None,
                             end = None):
        pass
    
    @property
    def recentWeeklyAlbumChart(self):
        return self.getWeeklyAlbumChart()
    
    def getWeeklyArtistChart(self,
                             start = None,
                             end = None):
        pass
    
    @property
    def recentWeeklyArtistChart(self):
        return self.getWeeklyArtistChart()
    
    def getWeeklyTrackChart(self,
                             start = None,
                             end = None):
        pass
    
    @property
    def recentWeeklyTrackChart(self):
        return self.getWeeklyTrackChart()
    
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

from api import Api
from error import LastfmError
from stats import Stats