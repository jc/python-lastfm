#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from cacheable import Cacheable
from taggable import Taggable
from sharable import Sharable
from searchable import Searchable
from lazylist import lazylist

class Track(LastfmBase, Cacheable, Sharable, Searchable, Taggable):
    """A class representing a track."""
    def init(self,
                 api,
                 name = None,
                 mbid = None,
                 url = None,
                 duration = None,
                 streamable = None,
                 full_track = None,
                 artist = None,
                 album = None,
                 position = None,
                 image = None,
                 stats = None,
                 played_on = None,
                 loved_on = None,
                 wiki = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        Taggable.init(self, api)
        Sharable.init(self, api)
        self._api = api
        self._id = id
        self._name = name
        self._mbid = mbid
        self._url = url
        self._duration = duration
        self._streamable = streamable
        self._full_track = full_track
        self._artist = artist
        self._album = album
        self._position = position
        self._image = image
        self._stats = stats and Stats(
                             subject = self,
                             match = stats.match,
                             playcount = stats.playcount,
                             rank = stats.rank,
                             listeners = stats.listeners,
                            )
        self._played_on = played_on
        self._loved_on = loved_on
        self._wiki = wiki and Wiki(
                         subject = self,
                         published = wiki.published,
                         summary = wiki.summary,
                         content = wiki.content
                        )

    @property
    def id(self):
        """id of the track"""
        return self._id

    @property
    def name(self):
        """name of the track"""
        return self._name

    @property
    def mbid(self):
        """mbid of the track"""
        return self._mbid

    @property
    def url(self):
        """url of the tracks's page"""
        return self._url

    @property
    def duration(self):
        """duration of the tracks's page"""
        return self._duration

    @property
    def streamable(self):
        """is the track streamable"""
        if self._streamable is None:
            self._fill_info()
        return self._streamable

    @property
    def full_track(self):
        """is the full track streamable"""
        if self._full_track is None:
            self._fill_info()
        return self._full_track

    @property
    def artist(self):
        """artist of the track"""
        return self._artist

    @property
    def album(self):
        """artist of the track"""
        if self._album is None:
            self._fill_info()
        return self._album

    @property
    def position(self):
        """position of the track"""
        if self._position is None:
            self._fill_info()
        return self._position

    @property
    def image(self):
        """image of the track's album cover"""
        return self._image

    @property
    def stats(self):
        """stats of the track"""
        return self._stats

    @property
    def played_on(self):
        """datetime the track was last played"""
        return self._played_on

    @property
    def loved_on(self):
        """datetime the track was marked 'loved'"""
        return self._loved_on

    @property
    def wiki(self):
        """wiki of the track"""
        if self._wiki == "na":
            return None
        if self._wiki is None:
            self._fill_info()
        return self._wiki

    @LastfmBase.cached_property
    def similar(self):
        """tracks similar to this track"""
        params = Track._check_params(
                                    {'method': 'track.getSimilar'},
                                    self.artist.name,
                                    self.name,
                                    self.mbid
                                    )
        data = self._api._fetch_data(params).find('similartracks')
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
                                      url = t.findtext('artist/url')
                                      ),
                      mbid = t.findtext('mbid'),
                      stats = Stats(
                                    subject = t.findtext('name'),
                                    match = float(t.findtext('match'))
                                    ),
                      streamable = (t.findtext('streamable') == '1'),
                      full_track = (t.find('streamable').attrib['fulltrack'] == '1'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      )
                for t in data.findall('track')
                ]

    @LastfmBase.top_property("similar")
    def most_similar(self):
        """track most similar to this track"""
        pass

    @LastfmBase.cached_property
    def top_fans(self):
        """top fans of the track"""
        params = Track._check_params(
                                    {'method': 'track.getTopFans'},
                                    self.artist.name,
                                    self.name,
                                    self.mbid
                                    )
        data = self._api._fetch_data(params).find('topfans')
        return [
                User(
                     self._api,
                     subject = self,
                     name = u.findtext('name'),
                     url = u.findtext('url'),
                     image = dict([(i.get('size'), i.text) for i in u.findall('image')]),
                     stats = Stats(
                                   subject = u.findtext('name'),
                                   weight = int(u.findtext('weight'))
                                   )
                     )
                for u in data.findall('user')
                ]

    @LastfmBase.top_property("top_fans")
    def top_fan(self):
        """topmost fan of the track"""
        pass

    @LastfmBase.cached_property
    def top_tags(self):
        """top tags for the track"""
        params = Track._check_params(
                                    {'method': 'track.getTopTags'},
                                    self.artist.name,
                                    self.name,
                                    self.mbid
                                    )
        data = self._api._fetch_data(params).find('toptags')
        return [
                Tag(
                    self._api,
                    subject = self,
                    name = t.findtext('name'),
                    url = t.findtext('url'),
                    stats = Stats(
                                  subject = t.findtext('name'),
                                  count = int(t.findtext('count')),
                                  )
                    )
                for t in data.findall('tag')
                ]

    @LastfmBase.top_property("top_tags")
    def top_tag(self):
        """topmost tag for the track"""
        pass

    def love(self):
        params = self._default_params({'method': 'track.love'})
        self._api._post_data(params)

    def ban(self):
        params = self._default_params({'method': 'track.ban'})
        self._api._post_data(params)

    @staticmethod
    def get_info(api,
                artist = None,
                track = None,
                mbid = None):
        data = Track._fetch_data(api, artist, track, mbid)
        t = Track(
                  api,
                  name = data.findtext('name'),
                  artist = Artist(
                                  api,
                                  name = data.findtext('artist/name'),
                                  ),
                  )
        t._fill_info()
        return t

    def _default_params(self, extra_params = {}):
        if not (self.artist and self.name):
            raise InvalidParametersError("artist and track have to be provided.")
        params = {'artist': self.artist.name, 'track': self.name}
        params.update(extra_params)
        return params

    @staticmethod
    def _search_yield_func(api, track):
        return Track(
                     api,
                     name = track.findtext('name'),
                     artist = Artist(
                                     api,
                                     name=track.findtext('artist')
                                     ),
                    url = track.findtext('url'),
                    stats = Stats(
                                  subject=track.findtext('name'),
                                  listeners=int(track.findtext('listeners'))
                                  ),
                    streamable = (track.findtext('streamable') == '1'),
                    full_track = (track.find('streamable').attrib['fulltrack'] == '1'),
                    image = dict([(i.get('size'), i.text) for i in track.findall('image')]),
                    )

    @staticmethod
    def _fetch_data(api,
                artist = None,
                track = None,
                mbid = None):
        params = Track._check_params({'method': 'track.getInfo'}, artist, track, mbid)
        return api._fetch_data(params).find('track')

    def _fill_info(self):
        data = Track._fetch_data(self._api, self.artist.name, self.name)
        self._id = int(data.findtext('id'))
        self._mbid = data.findtext('mbid')
        self._url = data.findtext('url')
        self._duration = int(data.findtext('duration'))
        self._streamable = (data.findtext('streamable') == '1'),
        self._full_track = (data.find('streamable').attrib['fulltrack'] == '1'),

        self._image = dict([(i.get('size'), i.text) for i in data.findall('image')])
        self._stats = Stats(
                       subject = self,
                       listeners = int(data.findtext('listeners')),
                       playcount = int(data.findtext('playcount')),
                       )
        self._artist = Artist(
                        self._api,
                        name = data.findtext('artist/name'),
                        mbid = data.findtext('artist/mbid'),
                        url = data.findtext('artist/url')
                        )
        self._album = Album(
                             self._api,
                             artist = self._artist,
                             name = data.findtext('album/title'),
                             mbid = data.findtext('album/mbid'),
                             url = data.findtext('album/url'),
                             image = dict([(i.get('size'), i.text) for i in data.findall('album/image')])
                             )
        self._position = int(data.find('album').attrib['position'])
        if data.find('wiki') is not None:
            self._wiki = Wiki(
                         self,
                         published = datetime(*(time.strptime(
                                                              data.findtext('wiki/published').strip(),
                                                              '%a, %d %b %Y %H:%M:%S +0000'
                                                              )[0:6])),
                         summary = data.findtext('wiki/summary'),
                         content = data.findtext('wiki/content')
                         )
        else:
            self._wiki = 'na'

    @staticmethod
    def _check_params(params,
                      artist = None,
                      track = None,
                      mbid = None):
        if not ((artist and track) or mbid):
            raise InvalidParametersError("either (artist and track) or mbid has to be given as argument.")

        if artist and track:
            params.update({'artist': artist, 'track': track})
        elif mbid:
            params.update({'mbid': mbid})
        return params

    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash("%s%s" % (kwds['name'], hash(kwds['artist'])))
        except KeyError:
            raise InvalidParametersError("name and artist have to be provided for hashing")

    def __hash__(self):
        return self.__class__._hash_func(name = self.name, artist = self.artist)

    def __eq__(self, other):
        if self.mbid and other.mbid:
            return self.mbid == other.mbid
        if self.url and other.url:
            return self.url == other.url
        if (self.name and self.artist) and (other.name and other.artist):
            return (self.name == other.name) and (self.artist == other.artist)
        return super(Track, self).__eq__(other)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.Track: '%s' by %s>" % (self.name, self.artist.name)

import time
from datetime import datetime

from api import Api
from artist import Artist
from album import Album
from error import InvalidParametersError
from stats import Stats
from tag import Tag
from user import User
from wiki import Wiki
