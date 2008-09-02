#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from lazylist import lazylist

class Group(LastfmBase):
    """A class representing a group on last.fm."""
    def init(self,
                 api,
                 name = None):
        if not isinstance(api, Api):
            raise LastfmInvalidParametersError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name

    @property
    def name(self):
        return self.__name

    @LastfmBase.cachedProperty
    def weeklyChartList(self):
        params = {'method': 'group.getweeklychartlist', 'group': self.name}
        data = self.__api._fetchData(params).find('weeklychartlist')
        return [
                WeeklyChart.createFromData(self.__api, self, c)
                for c in data.findall('chart')
                ]

    def getWeeklyAlbumChart(self,
                             start = None,
                             end = None):
        params = {'method': 'group.getweeklyalbumchart', 'group': self.name}
        params = WeeklyChart._checkWeeklyChartParams(params, start, end)
        data = self.__api._fetchData(params).find('weeklyalbumchart')
        return WeeklyAlbumChart.createFromData(self.__api, self, data)

    @LastfmBase.cachedProperty
    def recentWeeklyAlbumChart(self):
        return self.getWeeklyAlbumChart()
    
    @LastfmBase.cachedProperty
    def weeklyAlbumChartList(self):
        wcl = list(self.weeklyChartList)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                yield self.getWeeklyAlbumChart(wc.start, wc.end)
        return gen()

    def getWeeklyArtistChart(self,
                             start = None,
                             end = None):
        params = {'method': 'group.getweeklyartistchart', 'group': self.name}
        params = WeeklyChart._checkWeeklyChartParams(params, start, end)
        data = self.__api._fetchData(params).find('weeklyartistchart')
        return WeeklyArtistChart.createFromData(self.__api, self, data)

    @LastfmBase.cachedProperty
    def recentWeeklyArtistChart(self):
        return self.getWeeklyArtistChart()
    
    @LastfmBase.cachedProperty
    def weeklyArtistChartList(self):
        wcl = list(self.weeklyChartList)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                yield self.getWeeklyArtistChart(wc.start, wc.end)
        return gen()

    def getWeeklyTrackChart(self,
                             start = None,
                             end = None):
        params = {'method': 'group.getweeklytrackchart', 'group': self.name}
        params = WeeklyChart._checkWeeklyChartParams(params, start, end)
        data = self.__api._fetchData(params).find('weeklytrackchart')
        return WeeklyTrackChart.createFromData(self.__api, self, data)

    @LastfmBase.cachedProperty
    def recentWeeklyTrackChart(self):
        return self.getWeeklyTrackChart()
    
    @LastfmBase.cachedProperty
    def weeklyTrackChartList(self):
        wcl = list(self.weeklyChartList)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                yield self.getWeeklyTrackChart(wc.start, wc.end)
        return gen()

    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['name'])
        except KeyError:
            raise LastfmInvalidParametersError("name has to be provided for hashing")

    def __hash__(self):
        return self.__class__.hashFunc(name = self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.Group: %s>" % self.name

from api import Api
from error import LastfmInvalidParametersError
from weeklychart import WeeklyChart, WeeklyAlbumChart, WeeklyArtistChart, WeeklyTrackChart
