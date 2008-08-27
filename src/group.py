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

    @LastfmBase.cachedProperty
    def weeklyChartList(self):
        params = {'method': 'group.getweeklychartlist', 'group': self.name}
        data = self.__api._fetchData(params).find('weeklychartlist')
        return [
                WeeklyChart.createFromData(self.__api, self, c)
                for c in data.findall('chart')
                ]
    def _checkWeeklyChartParams(self, params, start = None, end = None):
        if (start is not None and end is None) or (start is None and end is not None):
            raise LastfmError("both start and end have to be provided.")
        if start is not None and end is not None:
            if isinstance(start, datetime) and isinstance(end, datetime):
                params.update({
                               'start': int(time.mktime(start.timetuple())),
                               'end': int(time.mktime(end.timetuple()))
                               })
            else:
                raise LastfmError("start and end must be datetime.datetime instances")

        return params

    def getWeeklyAlbumChart(self,
                             start = None,
                             end = None):
        params = {'method': 'group.getweeklyalbumchart', 'group': self.name}
        params = self._checkWeeklyChartParams(params, start, end)
        data = self.__api._fetchData(params).find('weeklyalbumchart')
        return WeeklyAlbumChart.createFromData(self.__api, self, data)

    @LastfmBase.cachedProperty
    def recentWeeklyAlbumChart(self):
        return self.getWeeklyAlbumChart()

    def getWeeklyArtistChart(self,
                             start = None,
                             end = None):
        params = {'method': 'group.getweeklyartistchart', 'group': self.name}
        params = self._checkWeeklyChartParams(params, start, end)
        data = self.__api._fetchData(params).find('weeklyartistchart')
        return WeeklyArtistChart.createFromData(self.__api, self, data)

    @LastfmBase.cachedProperty
    def recentWeeklyArtistChart(self):
        return self.getWeeklyArtistChart()

    def getWeeklyTrackChart(self,
                             start = None,
                             end = None):
        params = {'method': 'group.getweeklytrackchart', 'group': self.name}
        params = self._checkWeeklyChartParams(params, start, end)
        data = self.__api._fetchData(params).find('weeklytrackchart')
        return WeeklyTrackChart.createFromData(self.__api, self, data)

    @LastfmBase.cachedProperty
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

import time
from datetime import datetime

from api import Api
from error import LastfmError
from weeklychart import WeeklyChart, WeeklyAlbumChart, WeeklyArtistChart, WeeklyTrackChart
