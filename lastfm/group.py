#!/usr/bin/env python
"""Module for calling Group related last.fm web services API methods"""

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm"

from lastfm.base import LastfmBase
from lastfm.mixins import Cacheable
from lastfm.lazylist import lazylist
from lastfm.decorators import cached_property, depaginate

class Group(LastfmBase, Cacheable):
    """A class representing a group on last.fm."""
    def init(self, api, name = None, **kwargs):
        """
        Create a Group object by providing all the data related to it.
        
        @param api:    an instance of L{Api}
        @type api:     L{Api}
        @param name:   name of the group on last.fm
        @type name:    L{str}
        
        @raise InvalidParametersError: If an instance of L{Api} is not provided as the first
                                       parameter then an Exception is raised.
        """
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        self._api = api
        self._name = name

    @property
    def name(self):
        """
        name of the group
        @rtype: L{str}
        """
        return self._name

    @cached_property
    def weekly_chart_list(self):
        """
        a list of available weekly charts for this group
        @rtype: L{list} of L{WeeklyChart}
        """
        params = self._default_params({'method': 'group.getWeeklyChartList'})
        data = self._api._fetch_data(params).find('weeklychartlist')
        return [
                WeeklyChart.create_from_data(self._api, self, c)
                for c in data.findall('chart')
                ]

    def get_weekly_album_chart(self, start = None, end = None):
        """
        Get an album chart for the group, for a given date range.
        If no date range is supplied, it will return the most 
        recent album chart for the group. 
        
        @param start:    the date at which the chart should start from (optional)
        @type start:     C{datetime.datetime}
        @param end:      the date at which the chart should end on (optional)
        @type end:       C{datetime.datetime}
        
        @return:         an album chart for the group
        @rtype:          L{WeeklyAlbumChart}
        
        @raise InvalidParametersError: Both start and end parameter have to be either
                                       provided or not provided. Providing only one of
                                       them will raise an exception.
        """
        params = self._default_params({'method': 'group.getWeeklyAlbumChart'})
        params = WeeklyChart._check_chart_params(params, start, end)
        data = self._api._fetch_data(params).find('weeklyalbumchart')
        return WeeklyAlbumChart.create_from_data(self._api, self, data)

    @cached_property
    def recent_weekly_album_chart(self):
        """
        most recent album chart for the group
        @rtype: L{WeeklyAlbumChart}
        """
        return self.get_weekly_album_chart()
    
    @cached_property
    def weekly_album_chart_list(self):
        """
        a list of all album charts for this group in reverse-chronological
        order. (that means 0th chart is the most recent chart)
        @rtype: L{lazylist} of L{WeeklyAlbumChart}
        """
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                yield self.get_weekly_album_chart(wc.start, wc.end)
        return gen()

    def get_weekly_artist_chart(self, start = None, end = None):
        """
        Get an artist chart for the group, for a given date range.
        If no date range is supplied, it will return the most 
        recent artist chart for the group. 
        
        @param start:    the date at which the chart should start from (optional)
        @type start:     C{datetime.datetime}
        @param end:      the date at which the chart should end on (optional)
        @type end:       C{datetime.datetime}
        
        @return:         an artist chart for the group
        @rtype:          L{WeeklyArtistChart}
        
        @raise InvalidParametersError: Both start and end parameter have to be either
                                       provided or not provided. Providing only one of
                                       them will raise an exception.
        """
        params = self._default_params({'method': 'group.getWeeklyArtistChart'})
        params = WeeklyChart._check_chart_params(params, start, end)
        data = self._api._fetch_data(params).find('weeklyartistchart')
        return WeeklyArtistChart.create_from_data(self._api, self, data)

    @cached_property
    def recent_weekly_artist_chart(self):
        """
        most recent artist chart for the group
        @rtype: L{WeeklyArtistChart}
        """
        return self.get_weekly_artist_chart()
    
    @cached_property
    def weekly_artist_chart_list(self):
        """
        a list of all artist charts for this group in reverse-chronological
        order. (that means 0th chart is the most recent chart)
        @rtype: L{lazylist} of L{WeeklyArtistChart}
        """
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                yield self.get_weekly_artist_chart(wc.start, wc.end)
        return gen()

    def get_weekly_track_chart(self, start = None, end = None):
        """
        Get a track chart for the group, for a given date range.
        If no date range is supplied, it will return the most 
        recent artist chart for the group. 
        
        @param start:    the date at which the chart should start from (optional)
        @type start:     C{datetime.datetime}
        @param end:      the date at which the chart should end on (optional)
        @type end:       C{datetime.datetime}
        
        @return:         a track chart for the group
        @rtype:          L{WeeklyTrackChart}
        
        @raise InvalidParametersError: Both start and end parameter have to be either
                                       provided or not provided. Providing only one of
                                       them will raise an exception.
        """
        params = self._default_params({'method': 'group.getWeeklyTrackChart'})
        params = WeeklyChart._check_chart_params(params, start, end)
        data = self._api._fetch_data(params).find('weeklytrackchart')
        return WeeklyTrackChart.create_from_data(self._api, self, data)

    @cached_property
    def recent_weekly_track_chart(self):
        """
        most recent track chart for the group
        @rtype: L{WeeklyTrackChart}
        """
        return self.get_weekly_track_chart()
    
    @cached_property
    def weekly_track_chart_list(self):
        """
        a list of all track charts for this group in reverse-chronological
        order. (that means 0th chart is the most recent chart)
        @rtype: L{lazylist} of L{WeeklyTrackChart}
        """
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                yield self.get_weekly_track_chart(wc.start, wc.end)
        return gen()

    def get_weekly_tag_chart(self, start = None, end = None):
        """
        Get a tag chart for the group, for a given date range.
        If no date range is supplied, it will return the most 
        recent tag chart for the group. 
        
        @param start:    the date at which the chart should start from (optional)
        @type start:     C{datetime.datetime}
        @param end:      the date at which the chart should end on (optional)
        @type end:       C{datetime.datetime}
        
        @return:         a tag chart for the group
        @rtype:          L{WeeklyTagChart}
        
        @raise InvalidParametersError: Both start and end parameter have to be either
                                       provided or not provided. Providing only one of
                                       them will raise an exception.
                                       
        @note: This method is a composite method. It is not provided directly by the
               last.fm API. It uses other methods to collect the data, analyzes it and
               creates a chart. So this method is a little heavy to call, as it does
               mulitple calls to the API. 
        """
        WeeklyChart._check_chart_params({}, start, end)
        return WeeklyTagChart.create_from_data(self._api, self, start, end)

    @cached_property
    def recent_weekly_tag_chart(self):
        """
        most recent tag chart for the group
        @rtype: L{WeeklyTagChart}
        """
        return self.get_weekly_tag_chart()

    @cached_property
    def weekly_tag_chart_list(self):
        """
        a list of all tag charts for this group in reverse-chronological
        order. (that means 0th chart is the most recent chart)
        @rtype: L{lazylist} of L{WeeklyTagChart}
        """
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                try:
                    yield self.get_weekly_tag_chart(wc.start, wc.end)
                except LastfmError:
                    pass
        return gen()
    
    @cached_property
    @depaginate
    def members(self, page = None):
        """
        members of the group
        @rtype: L{lazylist} of L{User}
        """
        params = self._default_params({'method': 'group.getMembers'})
        if page is not None:
            params.update({'page': page})
        data = self._api._fetch_data(params).find('members')
        total_pages = int(data.attrib['totalPages'])
        yield total_pages
        for u in data.findall('user'):
            yield User(
                self._api,
                name = u.findtext('name'),
                real_name = u.findtext('realname'),
                image = dict([(i.get('size'), i.text) for i in u.findall('image')]),
                url = u.findtext('url')
            )
        
    def _default_params(self, extra_params = None):
        if not self.name:
            raise InvalidParametersError("group has to be provided.")
        params = {'group': self.name}
        if extra_params is not None:
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

from lastfm.api import Api
from lastfm.error import InvalidParametersError, LastfmError
from lastfm.user import User
from lastfm.chart import (WeeklyChart, WeeklyAlbumChart, 
    WeeklyArtistChart, WeeklyTrackChart, WeeklyTagChart)
