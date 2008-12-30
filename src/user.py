#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from lazylist import lazylist
import playlist

class User(LastfmBase):
    """A class representing an user."""
    def init(self,
                 api,
                 name = None,
                 url = None,
                 image = None,
                 stats = None,
                 language = None,
                 country = None,
                 age = None,
                 gender = None,
                 subscriber = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        self._api = api
        self._name = name
        self._url = url
        self._image = image
        self._stats = stats and Stats(
                             subject = self,
                             match = stats.match,
                             weight = stats.weight,
                             playcount = stats.playcount
                            )
        self._library = User.Library(api, self)
        self._language = language
        self._country = country
        self._age = age
        self._gender = gender
        self._subscriber = subscriber

    @property
    def name(self):
        """name of the user"""
        return self._name

    @property
    def url(self):
        """url of the user's page"""
        return self._url

    @property
    def image(self):
        """image of the user"""
        return self._image

    @property
    def stats(self):
        """stats for the user"""
        return self._stats

    @property
    def language(self):
        """lang for the user"""
        return self._language

    @property
    def country(self):
        """country for the user"""
        return self._country

    @property
    def age(self):
        """age for the user"""
        return self._age

    @property
    def gender(self):
        """stats for the user"""
        return self._gender

    @property
    def subscriber(self):
        """is the user a subscriber"""
        return self._subscriber

    @LastfmBase.cached_property
    def events(self):
        params = self._default_params({'method': 'user.getEvents'})
        data = self._api._fetch_data(params).find('events')

        return [
                Event.create_from_data(self._api, e)
                for e in data.findall('event')
                ]

    def get_past_events(self,
                      limit = None):
        params = self._default_params({'method': 'user.getPastEvents'})
        if limit is not None:
            params.update({'limit': limit})

        @lazylist
        def gen(lst):
            data = self._api._fetch_data(params).find('events')
            total_pages = int(data.attrib['totalPages'])

            @lazylist
            def gen2(lst, data):
                for e in data.findall('event'):
                    yield Event.create_from_data(self._api, e)

            for e in gen2(data):
                yield e

            for page in xrange(2, total_pages+1):
                params.update({'page': page})
                data = self._api._fetch_data(params).find('events')
                for e in gen2(data):
                    yield e
        return gen()

    @LastfmBase.cached_property
    def past_events(self):
        return self.get_past_events()

    def get_friends(self,
                   limit = None):
        params = self._default_params({'method': 'user.getFriends'})
        if limit is not None:
            params.update({'limit': limit})
        data = self._api._fetch_data(params).find('friends')
        return [
            User(
                self._api,
                subject = self,
                name = u.findtext('name'),
                image = dict([(i.get('size'), i.text) for i in u.findall('image')]),
                url = u.findtext('url'),
            )
            for u in data.findall('user')
        ]


    @LastfmBase.cached_property
    def friends(self):
        """friends of the user"""
        return self.get_friends()

    def get_neighbours(self, limit = None):
        params = self._default_params({'method': 'user.getNeighbours'})
        if limit is not None:
            params.update({'limit': limit})
        data = self._api._fetch_data(params).find('neighbours')
        return [
                User(
                    self._api,
                    subject = self,
                    name = u.findtext('name'),
                    image = {'medium': u.findtext('image')},
                    url = u.findtext('url'),
                    stats = Stats(
                                  subject = u.findtext('name'),
                                  match = u.findtext('match') and float(u.findtext('match')),
                                  ),
                )
                for u in data.findall('user')
            ]

    @LastfmBase.cached_property
    def neighbours(self):
        """neighbours of the user"""
        return self.get_neighbours()

    @LastfmBase.top_property("neighbours")
    def nearest_neighbour(self):
        """nearest neightbour of the user"""
        pass

    @LastfmBase.cached_property
    def playlists(self):
        """playlists of the user"""
        params = self._default_params({'method': 'user.getPlaylists'})
        data = self._api._fetch_data(params).find('playlists')
        return [
                User.Playlist(
                              self._api,
                              id = int(p.findtext('id')),
                              title = p.findtext('title'),
                              date = datetime(*(
                                                time.strptime(
                                                              p.findtext('date').strip(),
                                                              '%Y-%m-%dT%H:%M:%S'
                                                              )[0:6])
                              ),
                              size = int(p.findtext('size')),
                              creator = self
                              )
                for p in data.findall('playlist')
                ]

    @LastfmBase.cached_property
    def loved_tracks(self):
        params = self._default_params({'method': 'user.getLovedTracks'})
        data = self._api._fetch_data(params).find('lovedtracks')
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
                    image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                    loved_on = datetime(*(
                        time.strptime(
                            t.findtext('date').strip(),
                            '%d %b %Y, %H:%M'
                            )[0:6])
                        )
                    )
                for t in data.findall('track')
                ]

    def get_recent_tracks(self, limit = None):
        params = self._default_params({'method': 'user.getRecentTracks'})
        data = self._api._fetch_data(params, no_cache = True).find('recenttracks')
        return [
                Track(
                      self._api,
                      subject = self,
                      name = t.findtext('name'),
                      artist = Artist(
                                      self._api,
                                      subject = self,
                                      name = t.findtext('artist'),
                                      mbid = t.find('artist').attrib['mbid'],
                                      ),
                      album = Album(
                                    self._api,
                                    subject = self,
                                    name = t.findtext('album'),
                                    artist = Artist(
                                                    self._api,
                                                    subject = self,
                                                    name = t.findtext('artist'),
                                                    mbid = t.find('artist').attrib['mbid'],
                                                    ),
                                    mbid = t.find('album').attrib['mbid'],
                                    ),
                      mbid = t.findtext('mbid'),
                      streamable = (t.findtext('streamable') == '1'),
                      url = t.findtext('url'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      played_on = datetime(*(
                                           time.strptime(
                                                         t.findtext('date').strip(),
                                                         '%d %b %Y, %H:%M'
                                                         )[0:6])
                                           )
                      )
                      for t in data.findall('track')
                      ]

    @property
    def recent_tracks(self):
        """recent tracks played by the user"""
        return self.get_recent_tracks()

    @LastfmBase.top_property("recent_tracks")
    def most_recent_track(self):
        """most recent track played by the user"""
        pass

    def get_top_albums(self, period = None):
        params = self._default_params({'method': 'user.getTopAlbums'})
        if period is not None:
            params.update({'period': period})
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
                                   playcount = int(a.findtext('playcount')),
                                   rank = int(a.attrib['rank'])
                                   )
                     )
                for a in data.findall('album')
                ]

    @LastfmBase.cached_property
    def top_albums(self):
        """overall top albums of the user"""
        return self.get_top_albums()

    @LastfmBase.top_property("top_albums")
    def top_album(self):
        """overall top most album of the user"""
        pass

    def get_top_artists(self, period = None):
        params = self._default_params({'method': 'user.getTopArtists'})
        if period is not None:
            params.update({'period': period})
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
                                     playcount = a.findtext('playcount') and int(a.findtext('playcount')) or None
                                     ),
                       url = a.findtext('url'),
                       streamable = (a.findtext('streamable') == "1"),
                       image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                       )
                for a in data.findall('artist')
                ]

    @LastfmBase.cached_property
    def top_artists(self):
        """top artists of the user"""
        return self.get_top_artists()

    @LastfmBase.top_property("top_artists")
    def top_artist(self):
        """top artist of the user"""
        pass

    def get_top_tracks(self, period = None):
        params = self._default_params({'method': 'user.getTopTracks'})
        if period is not None:
            params.update({'period': period})
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
                                    playcount = t.findtext('playcount') and int(t.findtext('playcount')) or None
                                    ),
                      streamable = (t.findtext('streamable') == '1'),
                      full_track = (t.find('streamable').attrib['fulltrack'] == '1'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      )
                for t in data.findall('track')
                ]

    @LastfmBase.cached_property
    def top_tracks(self):
        """top tracks of the user"""
        return self.get_top_tracks()

    @LastfmBase.top_property("top_tracks")
    def top_track(self):
        """top track of the user"""
        return (len(self.top_tracks) and self.top_tracks[0] or None)

    def get_top_tags(self, limit = None):
        params = self._default_params({'method': 'user.getTopTags'})
        if limit is not None:
            params.update({'limit': limit})
        data = self._api._fetch_data(params).find('toptags')
        return [
                Tag(
                    self._api,
                    subject = self,
                    name = t.findtext('name'),
                    url = t.findtext('url'),
                    stats = Stats(
                                  subject = t.findtext('name'),
                                  count = int(t.findtext('count'))
                                  )
                    )
                for t in data.findall('tag')
                ]

    @LastfmBase.cached_property
    def top_tags(self):
        """top tags of the user"""
        return self.get_top_tags()

    @LastfmBase.top_property("top_tags")
    def top_tag(self):
        """top tag of the user"""
        pass

    @LastfmBase.cached_property
    def weekly_chart_list(self):
        params = self._default_params({'method': 'user.getWeeklyChartList'})
        data = self._api._fetch_data(params).find('weeklychartlist')
        return [
                WeeklyChart.create_from_data(self._api, self, c)
                for c in data.findall('chart')
                ]

    def get_weekly_album_chart(self,
                             start = None,
                             end = None):
        params = self._default_params({'method': 'user.getWeeklyAlbumChart'})
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
                try:
                    yield self.get_weekly_album_chart(wc.start, wc.end)
                except Error:
                    pass
        return gen()

    def get_weekly_artist_chart(self,
                             start = None,
                             end = None):
        params = self._default_params({'method': 'user.getWeeklyArtistChart'})
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
                try:
                    yield self.get_weekly_artist_chart(wc.start, wc.end)
                except Error:
                    pass
        return gen()

    def get_weekly_track_chart(self,
                             start = None,
                             end = None):
        params = self._default_params({'method': 'user.getWeeklyTrackChart'})
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
                try:
                    yield self.get_weekly_track_chart(wc.start, wc.end)
                except Error:
                    pass
        return gen()

    def compare(self, other, limit = None):
        return Tasteometer.compare(self._api,
                                   'user', 'user',
                                   self.name, other.name,
                                   limit)
    @property
    def library(self):
        return self._library

    @staticmethod
    def get_authenticated_user(api):
        data = api._fetch_data({'method': 'user.getInfo'}, sign = True, session = True).find('user')
        return User(
                api,
                name = data.findtext('name'),
                url = data.findtext('url'),
                language = data.findtext('lang'),
                country = Country(api, name = data.findtext('country')),
                age = int(data.findtext('age')),
                gender = data.findtext('gender'),
                subscriber = (data.findtext('subscriber') == '1'),
                stats = Stats(
                              subject = data.findtext('name'),
                              playcount = data.findtext('playcount')
                              )
            )

    def _default_params(self, extra_params = {}):
        if not self.name:
            raise InvalidParametersError("user has to be provided.")
        params = {'user': self.name}
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
        return "<lastfm.User: %s>" % self.name

    class Playlist(playlist.Playlist):
        """A class representing a playlist belonging to the user."""
        def init(self, api, id, title, date, size, creator):
            super(User.Playlist, self).init(api, "lastfm://playlist/%s" % id)
            self._id = id
            self._title = title
            self._date = date
            self._size = size
            self._creator = creator

        @property
        def id(self):
            return self._id

        @property
        def title(self):
            return self._title

        @property
        def date(self):
            return self._date

        @property
        def size(self):
            return self._size

        @property
        def creator(self):
            return self._creator

        def add_track(self, track):
            params = {'method': 'playlist.addTrack', 'playlistID': self.id}
            if not isinstance(track, Track):
                track = self._api.search_track(track)[0]

            params['artist'] = track.artist.name
            params['track'] = track.name
            self._api._post_data(params)

        @staticmethod
        def _hash_func(*args, **kwds):
            try:
                return hash(kwds['id'])
            except KeyError:
                raise InvalidParametersError("id has to be provided for hashing")

        def __hash__(self):
            return self.__class__._hash_func(id = self.id)

        def __repr__(self):
            return "<lastfm.User.Playlist: %s>" % self.title

    class Library(object):
        """A class representing the music library of the user."""
        def __init__(self, api, user):
            self._api = api
            self._user = user

        @property
        def user(self):
            return self._user

        def get_albums(self,
                      limit = None):
            params = self._default_params({'method': 'library.getAlbums'})
            if limit is not None:
                params.update({'limit': limit})

            @lazylist
            def gen(lst):
                data = self._api._fetch_data(params).find('albums')
                total_pages = int(data.attrib['totalPages'])

                @lazylist
                def gen2(lst, data):
                    for a in data.findall('album'):
                        yield Album(
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
                                                  playcount = int(a.findtext('playcount')),
                                                  )
                                    )


                for a in gen2(data):
                    yield a

                for page in xrange(2, total_pages+1):
                    params.update({'page': page})
                    try:
                        data = self._api._fetch_data(params).find('albums')
                    except Error:
                        continue
                    for a in gen2(data):
                        yield a
            return gen()

        @LastfmBase.cached_property
        def albums(self):
            return self.get_albums()

        def get_artists(self,
                       limit = None):
            params = self._default_params({'method': 'library.getArtists'})
            if limit is not None:
                params.update({'limit': limit})

            @lazylist
            def gen(lst):
                data = self._api._fetch_data(params).find('artists')
                total_pages = int(data.attrib['totalPages'])

                @lazylist
                def gen2(lst, data):
                    for a in data.findall('artist'):
                        yield Artist(
                                     self._api,
                                     subject = self,
                                     name = a.findtext('name'),
                                     mbid = a.findtext('mbid'),
                                     stats = Stats(
                                                   subject = a.findtext('name'),
                                                   playcount = a.findtext('playcount') and int(a.findtext('playcount')) or None,
                                                   tagcount = a.findtext('tagcount') and int(a.findtext('tagcount')) or None
                                                   ),
                                     url = a.findtext('url'),
                                     streamable = (a.findtext('streamable') == "1"),
                                     image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                                     )

                for a in gen2(data):
                    yield a

                for page in xrange(2, total_pages+1):
                    params.update({'page': page})
                    try:
                        data = self._api._fetch_data(params).find('artists')
                    except Error:
                        continue
                    for a in gen2(data):
                        yield a
            return gen()

        @LastfmBase.cached_property
        def artists(self):
            return self.get_artists()

        def get_tracks(self,
                      limit = None):
            params = self._default_params({'method': 'library.getTracks'})
            if limit is not None:
                params.update({'limit': limit})

            @lazylist
            def gen(lst):
                data = self._api._fetch_data(params).find('tracks')
                total_pages = int(data.attrib['totalPages'])

                @lazylist
                def gen2(lst, data):
                    for t in data.findall('track'):
                        yield Track(
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
                                                  playcount = t.findtext('playcount') and int(t.findtext('playcount')) or None,
                                                  tagcount = t.findtext('tagcount') and int(t.findtext('tagcount')) or None
                                                  ),
                                    streamable = (t.findtext('streamable') == '1'),
                                    full_track = (t.find('streamable').attrib['fulltrack'] == '1'),
                                    image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                                    )

                for t in gen2(data):
                    yield t

                for page in xrange(2, total_pages+1):
                    params.update({'page': page})
                    data = None
                    try:
                        data = self._api._fetch_data(params).find('tracks')
                    except Error:
                        continue
                    for t in gen2(data):
                        yield t
            return gen()

        @LastfmBase.cached_property
        def tracks(self):
            return self.get_tracks()

        def _default_params(self, extra_params = {}):
            if not self.user.name:
                raise InvalidParametersError("user has to be provided.")
            params = {'user': self.user.name}
            params.update(extra_params)
            return params

        @staticmethod
        def _hash_func(*args, **kwds):
            try:
                return hash(kwds['user'])
            except KeyError:
                raise InvalidParametersError("user has to be provided for hashing")

        def __hash__(self):
            return self.__class__._hash_func(user = self.user)

        def __repr__(self):
            return "<lastfm.User.Library: for user '%s'>" % self.user.name

from datetime import datetime
import time

from api import Api
from artist import Artist
from album import Album
from error import Error, InvalidParametersError
from event import Event
from geo import Country
from stats import Stats
from tag import Tag
from tasteometer import Tasteometer
from track import Track
from weeklychart import WeeklyChart, WeeklyAlbumChart, WeeklyArtistChart, WeeklyTrackChart
