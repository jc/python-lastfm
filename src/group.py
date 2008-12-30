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
            raise InvalidParametersError("api reference must be supplied as an argument")
        self._api = api
        self._name = name

    @property
    def name(self):
        return self._name

    @LastfmBase.cached_property
    def weekly_chart_list(self):
        params = self._default_params({'method': 'group.getWeeklyChartList'})
        data = self._api._fetch_data(params).find('weeklychartlist')
        return [
                WeeklyChart.create_from_data(self._api, self, c)
                for c in data.findall('chart')
                ]

    def get_weekly_album_chart(self,
                             start = None,
                             end = None):
        params = self._default_params({'method': 'group.getWeeklyAlbumChart'})
        params = WeeklyChart._check_weekly_chart_params(params, start, end)
        data = self._api._fetch_data(params).find('weeklyalbumchart')
        return WeeklyAlbumChart.create_from_data(self._api, self, data)

    @LastfmBase.cached_property
    def recent_weekly_album_chart(self):
        return self.get_weekly_album_chart()
    
    @LastfmBase.cached_property
    def weekly_album_chart_list(self):
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                yield self.get_weekly_album_chart(wc.start, wc.end)
        return gen()

    def get_weekly_artist_chart(self,
                             start = None,
                             end = None):
        params = self._default_params({'method': 'group.getWeeklyArtistChart'})
        params = WeeklyChart._check_weekly_chart_params(params, start, end)
        data = self._api._fetch_data(params).find('weeklyartistchart')
        return WeeklyArtistChart.create_from_data(self._api, self, data)

    @LastfmBase.cached_property
    def recent_weekly_artist_chart(self):
        return self.get_weekly_artist_chart()
    
    @LastfmBase.cached_property
    def weekly_artist_chart_list(self):
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                yield self.get_weekly_artist_chart(wc.start, wc.end)
        return gen()

    def get_weekly_track_chart(self,
                             start = None,
                             end = None):
        params = self._default_params({'method': 'group.getWeeklyTrackChart'})
        params = WeeklyChart._check_weekly_chart_params(params, start, end)
        data = self._api._fetch_data(params).find('weeklytrackchart')
        return WeeklyTrackChart.create_from_data(self._api, self, data)

    @LastfmBase.cached_property
    def recent_weekly_track_chart(self):
        return self.get_weekly_track_chart()
    
    @LastfmBase.cached_property
    def weekly_track_chart_list(self):
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                yield self.get_weekly_track_chart(wc.start, wc.end)
        return gen()

    def _default_params(self, extra_params = {}):
        if not self.name:
            raise InvalidParametersError("group has to be provided.")
        params = {'group': self.name}
        params.update(extra_params)
        return params
    
    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash(kwds['name'])
        except KeyError:
            raise InvalidParametersError("name has to be provided for hashing")

    def __hash__(self):
        return self.__class__._hash_func(name = self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.Group: %s>" % self.name

from api import Api
from error import InvalidParametersError
from weeklychart import WeeklyChart, WeeklyAlbumChart, WeeklyArtistChart, WeeklyTrackChart
