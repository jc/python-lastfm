#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Group(LastfmBase):
    """A class representing a group on last.fm."""
    def init(self,
                 api,
                 name = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name

    @property
    def name(self):
        return self.__name
    
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
        return "<lastfm.Group: %s>" % self.name

from api import Api
from error import LastfmError