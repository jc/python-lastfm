#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from lastfm.base import LastfmBase
from lastfm.mixins import Cacheable, Searchable, Sharable, Shoutable, Taggable
from lastfm.lazylist import lazylist

class Artist(LastfmBase, Cacheable, Sharable, Shoutable, Searchable, Taggable):
    """A class representing an artist."""
    def init(self,
                 api,
                 name = None,
                 mbid = None,
                 url = None,
                 image = None,
                 streamable = None,
                 stats = None,
                 similar = None,
                 top_tags = None,
                 bio = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        Sharable.init(self, api)
        Shoutable.init(self, api)
        Taggable.init(self, api)
        
        self._api = api
        self._name = name
        self._mbid = mbid
        self._url = url
        self._image = image
        self._streamable = streamable
        self._stats = stats and Stats(
                             subject = self,
                             listeners = stats.listeners,
                             playcount = stats.playcount,
                             weight = stats.weight,
                             match = stats.match,
                             rank = stats.rank
                            )
        self._similar = similar
        self._top_tags = top_tags
        self._bio = bio and Wiki(
                         subject = self,
                         published = bio.published,
                         summary = bio.summary,
                         content = bio.content
                        )

    @property
    def name(self):
        """name of the artist"""
        return self._name

    @property
    def mbid(self):
        """mbid of the artist"""
        if self._mbid is None:
            self._fill_info()
        return self._mbid

    @property
    def url(self):
        """url of the artist's page"""
        if self._url is None:
            self._fill_info()
        return self._url

    @property
    def image(self):
        """images of the artist"""
        if self._image is None:
            self._fill_info()
        return self._image

    @property
    def streamable(self):
        """is the artist streamable"""
        if self._streamable is None:
            self._fill_info()
        return self._streamable

    @property
    def stats(self):
        """stats for the artist"""
        if self._stats is None:
            self._fill_info()
        return self._stats

    def get_similar(self, limit = None):
        params = self._default_params({'method': 'artist.getSimilar'})
        if limit is not None:
            params.update({'limit': limit})
        data = self._api._fetch_data(params).find('similarartists')
        self._similar = [
                          Artist(
                                 self._api,
                                 subject = self,
                                 name = a.findtext('name'),
                                 mbid = a.findtext('mbid'),
                                 stats = Stats(
                                               subject = a.findtext('name'),
                                               match = float(a.findtext('match')),
                                               ),
                                 url = 'http://' + a.findtext('url'),
                                 image = {'large': a.findtext('image')}
                                 )
                          for a in data.findall('artist')
                          ]
        return self._similar[:]

    @property
    def similar(self):
        """artists similar to this artist"""
        if self._similar is None or len(self._similar) < 6:
            return self.get_similar()
        return self._similar[:]

    @LastfmBase.top_property("similar")
    def most_similar(self):
        """artist most similar to this artist"""
        pass

    @property
    def top_tags(self):
        """top tags for the artist"""
        if self._top_tags is None or len(self._top_tags) < 6:
            params = self._default_params({'method': 'artist.getTopTags'})
            data = self._api._fetch_data(params).find('toptags')
            self._top_tags = [
                              Tag(
                                  self._api,
                                  subject = self,
                                  name = t.findtext('name'),
                                  url = t.findtext('url')
                                  )
                              for t in data.findall('tag')
                              ]
        return self._top_tags[:]

    @LastfmBase.top_property("top_tags")
    def top_tag(self):
        """top tag for the artist"""
        pass

    @property
    def bio(self):
        """biography of the artist"""
        if self._bio is None:
            self._fill_info()
        return self._bio

    @LastfmBase.cached_property
    def events(self):
        """events for the artist"""
        params = self._default_params({'method': 'artist.getEvents'})
        data = self._api._fetch_data(params).find('events')

        return [
                Event.create_from_data(self._api, e)
                for e in data.findall('event')
                ]

    @LastfmBase.cached_property
    def top_albums(self):
        """top albums of the artist"""
        params = self._default_params({'method': 'artist.getTopAlbums'})
        data = self._api._fetch_data(params).find('topalbums')

        return [
                Album(
                     self._api,
                     subject = self,
                     name = a.findtext('name'),
                     artist = self,
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

    @LastfmBase.top_property("top_albums")
    def top_album(self):
        """top album of the artist"""
        pass

    @LastfmBase.cached_property
    def top_fans(self):
        """top fans of the artist"""
        params = self._default_params({'method': 'artist.getTopFans'})
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
        """top fan of the artist"""
        pass

    @LastfmBase.cached_property
    def top_tracks(self):
        """top tracks of the artist"""
        params = self._default_params({'method': 'artist.getTopTracks'})
        data = self._api._fetch_data(params).find('toptracks')
        return [
                Track(
                      self._api,
                      subject = self,
                      name = t.findtext('name'),
                      artist = self,
                      mbid = t.findtext('mbid'),
                      stats = Stats(
                                    subject = t.findtext('name'),
                                    playcount = int(t.findtext('playcount')),
                                    rank = int(t.attrib['rank'])
                                    ),
                      streamable = (t.findtext('streamable') == '1'),
                      full_track = (t.find('streamable').attrib['fulltrack'] == '1'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      )
                for t in data.findall('track')
                ]

    @LastfmBase.top_property("top_tracks")
    def top_track(self):
        """topmost fan of the artist"""
        pass

    @staticmethod
    def get_info(api,
                artist = None,
                mbid = None):
        data = Artist._fetch_data(api, artist, mbid)

        a = Artist(api, name = data.findtext('name'))
        a._fill_info()
        return a

    def _default_params(self, extra_params = {}):
        if not self.name:
            raise InvalidParametersError("artist has to be provided.")
        params = {'artist': self.name}
        params.update(extra_params)
        return params

    @staticmethod
    def _fetch_data(api,
                artist = None,
                mbid = None):
        params = {'method': 'artist.getInfo'}
        if not (artist or mbid):
            raise InvalidParametersError("either artist or mbid has to be given as argument.")
        if artist:
            params.update({'artist': artist})
        elif mbid:
            params.update({'mbid': mbid})
        return api._fetch_data(params).find('artist')

    def _fill_info(self):
        data = Artist._fetch_data(self._api, self.name)
        self._name = data.findtext('name')
        self._mbid = data.findtext('mbid')
        self._url = data.findtext('url')
        self._image = dict([(i.get('size'), i.text) for i in data.findall('image')])
        self._streamable = (data.findtext('streamable') == 1)
        if not self._stats:
            self._stats = Stats(
                             subject = self,
                             listeners = int(data.findtext('stats/listeners')),
                             playcount = int(data.findtext('stats/playcount'))
                             )
        self._similar = [
                          Artist(
                                 self._api,
                                 subject = self,
                                 name = a.findtext('name'),
                                 url = a.findtext('url'),
                                 image = dict([(i.get('size'), i.text) for i in a.findall('image')])
                                 )
                          for a in data.findall('similar/artist')
                          ]
        self._top_tags = [
                          Tag(
                              self._api,
                              subject = self,
                              name = t.findtext('name'),
                              url = t.findtext('url')
                              )
                          for t in data.findall('tags/tag')
                          ]
        self._bio = Wiki(
                         self,
                         published = data.findtext('bio/published').strip() and
                                        datetime(*(time.strptime(
                                                              data.findtext('bio/published').strip(),
                                                              '%a, %d %b %Y %H:%M:%S +0000'
                                                              )[0:6])),
                         summary = data.findtext('bio/summary'),
                         content = data.findtext('bio/content')
                         )

    @staticmethod
    def _search_yield_func(api, artist):
        return Artist(
                      api,
                      name = artist.findtext('name'),
                      mbid = artist.findtext('mbid'),
                      url = artist.findtext('url'),
                      image = dict([(i.get('size'), i.text) for i in artist.findall('image')]),
                      streamable = (artist.findtext('streamable') == '1'),
                      )
    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash(kwds['name'].lower())
        except KeyError:
            try:
                return hash(args[1].lower())
            except IndexError:
                raise InvalidParametersError("name has to be provided for hashing")

    def __hash__(self):
        return self.__class__._hash_func(name = self.name)

    def __eq__(self, other):
        if self.mbid and other.mbid:
            return self.mbid == other.mbid
        if self.url and other.url:
            return self.url == other.url
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.Artist: %s>" % self._name

from datetime import datetime
import time

from lastfm.album import Album
from lastfm.api import Api
from lastfm.error import InvalidParametersError
from lastfm.event import Event
from lastfm.stats import Stats
from lastfm.tag import Tag
from lastfm.track import Track
from lastfm.user import User
from lastfm.wiki import Wiki
