#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from taggable import Taggable
from sharable import Sharable
from searchable import Searchable
from lazylist import lazylist

class Track(LastfmBase, Taggable, Sharable, Searchable):
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
        self.__api = api
        self.__id = id
        self.__name = name
        self.__mbid = mbid
        self.__url = url
        self.__duration = duration
        self.__streamable = streamable
        self.__full_track = full_track
        self.__artist = artist
        self.__album = album
        self.__position = position
        self.__image = image
        self.__stats = stats and Stats(
                             subject = self,
                             match = stats.match,
                             playcount = stats.playcount,
                             rank = stats.rank,
                             listeners = stats.listeners,
                            )
        self.__played_on = played_on
        self.__loved_on = loved_on
        self.__wiki = wiki and Wiki(
                         subject = self,
                         published = wiki.published,
                         summary = wiki.summary,
                         content = wiki.content
                        )
    
    @property
    def id(self):
        """id of the track"""
        return self.__id
        
    @property
    def name(self):
        """name of the track"""
        return self.__name

    @property
    def mbid(self):
        """mbid of the track"""
        return self.__mbid

    @property
    def url(self):
        """url of the tracks's page"""
        return self.__url
    
    @property
    def duration(self):
        """duration of the tracks's page"""
        return self.__duration

    @property
    def streamable(self):
        """is the track streamable"""
        if self.__streamable is None:
            self._fill_info()
        return self.__streamable

    @property
    def full_track(self):
        """is the full track streamable"""
        if self.__full_track is None:
            self._fill_info()
        return self.__full_track
    
    @property
    def artist(self):
        """artist of the track"""
        return self.__artist

    @property
    def album(self):
        """artist of the track"""
        if self.__album is None:
            self._fill_info()
        return self.__album

    @property
    def position(self):
        """position of the track"""
        if self.__position is None:
            self._fill_info()
        return self.__position
    
    @property
    def image(self):
        """image of the track's album cover"""
        return self.__image

    @property
    def stats(self):
        """stats of the track"""
        return self.__stats

    @property
    def playedOn(self):
        """datetime the track was last played"""
        return self.__played_on

    @property
    def lovedOn(self):
        """datetime the track was marked 'loved'"""
        return self.__loved_on
    
    @property
    def wiki(self):
        """wiki of the track"""
        if self.__wiki == "na":
            return None
        if self.__wiki is None:
            self._fill_info()
        return self.__wiki
    
    def _default_params(self, extra_params = None):
        if not (self.artist and self.name):
            raise InvalidParametersError("artist and track have to be provided.")
        params = {'artist': self.artist.name, 'track': self.name}
        if extra_params is not None:
            params.update(extra_params)
        return params

    @LastfmBase.cachedProperty
    def similar(self):
        """tracks similar to this track"""
        params = Track._check_params(
                                    {'method': 'track.getSimilar'},
                                    self.artist.name,
                                    self.name,
                                    self.mbid
                                    )
        data = self.__api._fetch_data(params).find('similartracks')
        return [
                Track(
                      self.__api,
                      subject = self,
                      name = t.findtext('name'),
                      artist = Artist(
                                      self.__api,
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
                      fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      )
                for t in data.findall('track')
                ]

    @LastfmBase.topProperty("similar")
    def most_similar(self):
        """track most similar to this track"""
        pass

    @LastfmBase.cachedProperty
    def top_fans(self):
        """top fans of the track"""
        params = Track._check_params(
                                    {'method': 'track.getTopFans'},
                                    self.artist.name,
                                    self.name,
                                    self.mbid
                                    )
        data = self.__api._fetch_data(params).find('topfans')
        return [
                User(
                     self.__api,
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

    @LastfmBase.topProperty("top_fans")
    def top_fan(self):
        """topmost fan of the track"""
        pass

    @LastfmBase.cachedProperty
    def top_tags(self):
        """top tags for the track"""
        params = Track._check_params(
                                    {'method': 'track.getTopTags'},
                                    self.artist.name,
                                    self.name,
                                    self.mbid
                                    )
        data = self.__api._fetch_data(params).find('toptags')
        return [
                Tag(
                    self.__api,
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

    @LastfmBase.topProperty("top_tags")
    def top_tag(self):
        """topmost tag for the track"""
        pass
    
    def love(self):
        params = self._default_params({'method': 'track.love'})
        self.__api._post_data(params)
        
    def ban(self):
        params = self._default_params({'method': 'track.ban'})
        self.__api._post_data(params)

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
                    fullTrack = (track.find('streamable').attrib['fulltrack'] == '1'),
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
        data = Track._fetch_data(self.__api, self.artist.name, self.name)
        self.__id = int(data.findtext('id'))
        self.__mbid = data.findtext('mbid')
        self.__url = data.findtext('url')
        self.__duration = int(data.findtext('duration'))
        self.__streamable = (data.findtext('streamable') == '1'),
        self.__full_track = (data.find('streamable').attrib['fulltrack'] == '1'),
                                
        self.__image = dict([(i.get('size'), i.text) for i in data.findall('image')])
        self.__stats = Stats(
                       subject = self,
                       listeners = int(data.findtext('listeners')),
                       playcount = int(data.findtext('playcount')),
                       )
        self.__artist = Artist(
                        self.__api,
                        name = data.findtext('artist/name'),
                        mbid = data.findtext('artist/mbid'),
                        url = data.findtext('artist/url')
                        )
        self.__album = Album(
                             self.__api,
                             artist = self.__artist,
                             name = data.findtext('album/title'),
                             mbid = data.findtext('album/mbid'),
                             url = data.findtext('album/url'),
                             image = dict([(i.get('size'), i.text) for i in data.findall('album/image')])
                             )
        self.__position = int(data.find('album').attrib['position'])
        if data.find('wiki') is not None:
            self.__wiki = Wiki(
                         self,
                         published = datetime(*(time.strptime(
                                                              data.findtext('wiki/published').strip(),
                                                              '%a, %d %b %Y %H:%M:%S +0000'
                                                              )[0:6])),
                         summary = data.findtext('wiki/summary'),
                         content = data.findtext('wiki/content')
                         )
        else:
            self.__wiki = 'na'
                         
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
    def hash_func(*args, **kwds):
        try:
            return hash("%s%s" % (kwds['name'], hash(kwds['artist'])))
        except KeyError:
            raise InvalidParametersError("name and artist have to be provided for hashing")

    def __hash__(self):
        return self.__class__.hash_func(name = self.name, artist = self.artist)

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