#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm"

from lastfm.base import LastfmBase
from lastfm.mixins import Cacheable, Searchable
from lastfm.lazylist import lazylist
from lastfm.decorators import cached_property, top_property

class Tag(LastfmBase, Cacheable, Searchable):
    """A class representing a tag."""
    def init(self,
                 api,
                 name = None,
                 url = None,
                 streamable = None,
                 stats = None,
                 **kwargs):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        self._api = api
        self._name = name
        self._url = url
        self._streamable = streamable
        self._stats = stats and Stats(
                             subject = self,
                             count = stats.count,
                             rank = stats.rank
                             )

    @property
    def name(self):
        """name of the tag"""
        return self._name

    @property
    def url(self):
        """url of the tag's page"""
        return self._url

    @property
    def streamable(self):
        """is the tag streamable"""
        return self._streamable

    @property
    def stats(self):
        return self._stats

    @cached_property
    def similar(self):
        """tags similar to this tag"""
        params = self._default_params({'method': 'tag.getSimilar'})
        data = self._api._fetch_data(params).find('similartags')
        return [
                Tag(
                    self._api,
                    subject = self,
                    name = t.findtext('name'),
                    url = t.findtext('url'),
                    streamable = (t.findtext('streamable') == "1"),
                    )
                for t in data.findall('tag')
                ]

    @top_property("similar")
    def most_similar(self):
        """most similar tag to this tag"""
        pass

    @cached_property
    def top_albums(self):
        """top albums for the tag"""
        params = self._default_params({'method': 'tag.getTopAlbums'})
        data = self._api._fetch_data(params).find('topalbums')
        return [
                Album(
                      self._api,
                      subject = self,
                      name = a.findtext('name'),
                      artist = Artist(
                                      self._api,
                                      subject = self,
                                      name = a.findtext('artist/name'),
                                      mbid = a.findtext('artist/mbid'),
                                      url = a.findtext('artist/url'),
                                      ),
                      mbid = a.findtext('mbid'),
                      url = a.findtext('url'),
                      image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                      stats = Stats(
                                    subject = a.findtext('name'),
                                    tagcount = a.findtext('tagcount') and int(a.findtext('tagcount')) or None,
                                    rank = a.attrib['rank'].strip() and int(a.attrib['rank']) or None
                                    )
                      )
                for a in data.findall('album')
                ]

    @top_property("top_albums")
    def top_album(self):
        """top album for the tag"""
        pass

    @cached_property
    def top_artists(self):
        """top artists for the tag"""
        params = self._default_params({'method': 'tag.getTopArtists'})
        data = self._api._fetch_data(params).find('topartists')
        return [
                Artist(
                       self._api,
                       subject = self,
                       name = a.findtext('name'),
                       mbid = a.findtext('mbid'),
                       stats = Stats(
                                     subject = a.findtext('name'),
                                     rank = a.attrib['rank'].strip() and int(a.attrib['rank']) or None,
                                     tagcount = a.findtext('tagcount') and int(a.findtext('tagcount')) or None
                                     ),
                       url = a.findtext('url'),
                       streamable = (a.findtext('streamable') == "1"),
                       image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                       )
                for a in data.findall('artist')
                ]

    @top_property("top_artists")
    def top_artist(self):
        """top artist for the tag"""
        pass

    @cached_property
    def top_tracks(self):
        """top tracks for the tag"""
        params = self._default_params({'method': 'tag.getTopTracks'})
        data = self._api._fetch_data(params).find('toptracks')
        return [
                Track(
                      self._api,
                      subject = self,
                      name = t.findtext('name'),
                      artist = Artist(
                                      self._api,
                                      subject = self,
                                      name = t.findtext('artist/name'),
                                      mbid = t.findtext('artist/mbid'),
                                      url = t.findtext('artist/url'),
                                      ),
                      mbid = t.findtext('mbid'),
                      stats = Stats(
                                    subject = t.findtext('name'),
                                    rank = t.attrib['rank'].strip() and int(t.attrib['rank']) or None,
                                    tagcount = t.findtext('tagcount') and int(t.findtext('tagcount')) or None
                                    ),
                      streamable = (t.findtext('streamable') == '1'),
                      full_track = (t.find('streamable').attrib['fulltrack'] == '1'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      )
                for t in data.findall('track')
                ]

    @top_property("top_tracks")
    def top_track(self):
        """top track for the tag"""
        pass

    @cached_property
    def playlist(self):
        return Playlist.fetch(self._api,
                              "lastfm://playlist/tag/%s/freetracks" % self.name)

    @cached_property
    def weekly_chart_list(self):
        params = self._default_params({'method': 'tag.getWeeklyChartList'})
        data = self._api._fetch_data(params).find('weeklychartlist')
        return [
                WeeklyChart.create_from_data(self._api, self, c)
                for c in data.findall('chart')
                ]

    def get_weekly_artist_chart(self,
                             start = None,
                             end = None,
                             limit = None):
        params = self._default_params({'method': 'tag.getWeeklyArtistChart'})
        if limit is not None:
            params['limit'] = limit
        params = WeeklyArtistChart._check_weekly_chart_params(params, start, end)
        data = self._api._fetch_data(params).find('weeklyartistchart')
        return WeeklyArtistChart.create_from_data(self._api, self, data)

    @cached_property
    def recent_weekly_artist_chart(self):
        return self.get_weekly_artist_chart()

    @cached_property
    def weekly_artist_chart_list(self):
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                try:
                    yield self.get_weekly_artist_chart(wc.start, wc.end)
                except LastfmError:
                    pass
        return gen()
    
    @staticmethod
    def get_top_tags(api):
        params = {'method': 'tag.getTopTags'}
        data = api._fetch_data(params).find('toptags')
        return [
                Tag(
                    api,
                    name = t.findtext('name'),
                    url = t.findtext('url'),
                    stats = Stats(
                                  subject = t.findtext('name'),
                                  count = int(t.findtext('count')),
                                  )
                    )
                for t in data.findall('tag')
                ]

    def _default_params(self, extra_params = {}):
        if not self.name:
            raise InvalidParametersError("tag has to be provided.")
        params = {'tag': self.name}
        params.update(extra_params)
        return params

    @staticmethod
    def _search_yield_func(api, tag):
        return Tag(
                   api,
                   name = tag.findtext('name'),
                   url = tag.findtext('url'),
                   stats = Stats(
                                 subject = tag.findtext('name'),
                                 count = int(tag.findtext('count')),
                                 )
                    )

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
        return "<lastfm.Tag: %s>" % self.name

from lastfm.album import Album
from lastfm.api import Api
from lastfm.artist import Artist
from lastfm.error import LastfmError, InvalidParametersError
from lastfm.playlist import Playlist
from lastfm.stats import Stats
from lastfm.track import Track
from lastfm.weeklychart import WeeklyChart, WeeklyArtistChart