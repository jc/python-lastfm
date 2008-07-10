#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Group(object):
    """A class representing a group on last.fm."""
    def __init__(self,
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