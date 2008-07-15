#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Group(LastfmBase):
    """A class representing a group on last.fm."""
    def init(self,
                 api,
                 name = None):
        self.__api = api
        self.__name = name

    def getName(self):
        return self.__name
    
    name = property(getName, None, None, "Name's Docstring")
    
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
        return "<lastfm.Group: %s>" % self.name

from error import LastfmError