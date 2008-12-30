#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from taggable import Taggable

class Album(Taggable, LastfmBase):
    """A class representing an album."""
    def init(self,
                 api,
                 name = None,
                 artist = None,
                 id = None,
                 mbid = None,
                 url = None,
                 release_date = None,
                 image = None,
                 stats = None,
                 top_tags = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        Taggable.init(self, api)
        self.__api = api
        self.__name = name
        self.__artist = artist
        self.__id = id
        self.__mbid = mbid
        self.__url = url
        self.__release_date = release_date
        self.__image = image
        self.__stats = stats and Stats(
                             subject = self,
                             listeners = stats.listeners,
                             playcount = stats.playcount,
                             match = stats.match,
                             rank = stats.rank
                            )
        self.__top_tags = top_tags
    
    @property
    def name(self):
        """name of the album"""
        return self.__name
    
    @property
    def artist(self):
        """artist of the album"""
        return self.__artist
    
    @property
    def id(self):
        """id of the album"""
        if self.__id is None:
            self._fill_info()
        return self.__id

    @property
    def mbid(self):
        """mbid of the album"""
        if self.__mbid is None:
            self._fill_info()
        return self.__mbid

    @property
    def url(self):
        """url of the album's page"""
        if self.__url is None:
            self._fill_info()
        return self.__url

    @property
    def release_date(self):
        """release date of the album"""
        if self.__release_date is None:
            self._fill_info()
        return self.__release_date

    @property
    def image(self):
        """cover images of the album"""
        if self.__image is None:
            self._fill_info()
        return self.__image

    @property
    def stats(self):
        """stats related to the album"""
        if self.__stats is None:
            self._fill_info()
        return self.__stats

    @LastfmBase.cachedProperty
    def top_tags(self):
        """top tags for the album"""
        params = {'method': 'album.getInfo'}
        if self.artist and self.name:
            params.update({'artist': self.artist.name, 'album': self.name})
        elif self.mbid:
            params.update({'mbid': self.mbid})
        data = self.__api._fetch_data(params).find('album')
        return [
                Tag(
                    self.__api,
                    subject = self,
                    name = t.findtext('name'),
                    url = t.findtext('url')
                    )
                for t in data.findall('toptags/tag')
                ]

    @LastfmBase.topProperty("top_tags")
    def top_tag(self):
        """top tag for the album"""
        pass
    
    @LastfmBase.cachedProperty
    def playlist(self):
        return Playlist.fetch(self.__api, "lastfm://playlist/album/%s" % self.id)
    
    def _default_params(self, extra_params = None):
        if not (self.artist and self.name):
            raise InvalidParametersError("artist and album have to be provided.")
        params = {'artist': self.artist.name, 'album': self.name}
        if extra_params is not None:
            params.update(extra_params)
        return params
    
    @staticmethod
    def _fetch_data(api,
                artist = None,
                album = None,
                mbid = None):
        params = {'method': 'album.getInfo'}
        if not ((artist and album) or mbid):
            raise InvalidParametersError("either (artist and album) or mbid has to be given as argument.")
        if artist and album:
            params.update({'artist': artist, 'album': album})
        elif mbid:
            params.update({'mbid': mbid})
        return api._fetch_data(params).find('album')
    
    def _fill_info(self):
        data = Album._fetch_data(self.__api, self.artist.name, self.name)
        self.__id = int(data.findtext('id'))
        self.__mbid = data.findtext('mbid')
        self.__url = data.findtext('url')
        self.__release_date = data.findtext('releasedate') and data.findtext('releasedate').strip() and \
                            datetime(*(time.strptime(data.findtext('releasedate').strip(), '%d %b %Y, 00:00')[0:6]))
        self.__image = dict([(i.get('size'), i.text) for i in data.findall('image')])
        self.__stats = Stats(
                       subject = self,
                       listeners = int(data.findtext('listeners')),
                       playcount = int(data.findtext('playcount')),
                       )
        self.__top_tags = [
                    Tag(
                        self.__api,
                        subject = self,
                        name = t.findtext('name'),
                        url = t.findtext('url')
                        ) 
                    for t in data.findall('toptags/tag')
                    ]
                         
    @staticmethod
    def get_info(api,
                artist = None,
                album = None,
                mbid = None):
        data = Album._fetch_data(api, artist, album, mbid)
        a = Album(
                  api,
                  name = data.findtext('name'),
                  artist = Artist(
                                  api,
                                  name = data.findtext('artist'),
                                  ),
                  )
        a._fill_info()
        return a
        
    @staticmethod
    def hash_func(*args, **kwds):
        try:
            return hash("%s%s" % (kwds['name'], hash(kwds['artist'])))
        except KeyError:
            raise InvalidParametersError("name and artist have to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hash_func(name = self.name, artist = self.artist)
        
    def __eq__(self, other):
        if self.id and other.id:
            return self.id == other.id
        if self.mbid and other.mbid:
            return self.mbid == other.mbid
        if self.url and other.url:
            return self.url == other.url
        if (self.name and self.artist) and (other.name and other.artist):
            return (self.name == other.name) and (self.artist == other.artist)
        return super(Album, self).__eq__(other)
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __repr__(self):
        return "<lastfm.Album: '%s' by %s>" % (self.name, self.artist.name)
        
                     
from datetime import datetime
import time

from api import Api
from artist import Artist
from error import InvalidParametersError
from playlist import Playlist
from stats import Stats
from tag import Tag