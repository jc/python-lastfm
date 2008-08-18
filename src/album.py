#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Album(LastfmBase):
    """A class representing an album."""
    def init(self,
                 api,
                 name = None,
                 artist = None,
                 id = None,
                 mbid = None,
                 url = None,
                 releaseDate = None,
                 image = None,
                 stats = None,
                 topTags = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__artist = artist
        self.__id = id
        self.__mbid = mbid
        self.__url = url
        self.__releaseDate = releaseDate
        self.__image = image
        self.__stats = stats and Stats(
                             subject = self,
                             listeners = stats.listeners,
                             playcount = stats.playcount,
                             match = stats.match,
                             rank = stats.rank
                            )
        self.__topTags = topTags
    
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
            self._fillInfo()
        return self.__id

    @property
    def mbid(self):
        """mbid of the album"""
        if self.__mbid is None:
            self._fillInfo()
        return self.__mbid

    @property
    def url(self):
        """url of the album's page"""
        if self.__url is None:
            self._fillInfo()
        return self.__url

    @property
    def releaseDate(self):
        """release date of the album"""
        if self.__releaseDate is None:
            self._fillInfo()
        return self.__releaseDate

    @property
    def image(self):
        """cover images of the album"""
        if self.__image is None:
            self._fillInfo()
        return self.__image

    @property
    def stats(self):
        """stats related to the album"""
        if self.__stats is None:
            self._fillInfo()
        return self.__stats

    @property
    def topTags(self):
        """top tags for the album"""
        if self.__topTags is None:
            params = {'method': 'album.getinfo'}
            if self.artist and self.name:
                params.update({'artist': self.artist.name, 'album': self.name})
            elif self.mbid:
                params.update({'mbid': self.mbid})
            data = self.__api._fetchData(params).find('album')
            self.__topTags = [
                              Tag(
                                  self.__api,
                                  name = t.findtext('name'),
                                  url = t.findtext('url')
                                  ) 
                              for t in data.findall('toptags/tag')
                              ]
        return self.__topTags

    @property
    def topTag(self):
        """top tag for the album"""
        return (self.topTags and len(self.topTags) and self.topTags[0] or None)
    
    @staticmethod
    def _fetchData(api,
                artist = None,
                album = None,
                mbid = None):
        params = {'method': 'album.getinfo'}
        if not ((artist and album) or mbid):
            raise LastfmError("either (artist and album) or mbid has to be given as argument.")
        if artist and album:
            params.update({'artist': artist, 'album': album})
        elif mbid:
            params.update({'mbid': mbid})
        return api._fetchData(params).find('album')
    
    def _fillInfo(self):
        data = Album._fetchData(self.__api, self.artist.name, self.name)
        self.__id = int(data.findtext('id'))
        self.__mbid = data.findtext('mbid')
        self.__url = data.findtext('url')
        self.__releaseDate = data.findtext('releasedate') and data.findtext('releasedate').strip() and \
                            datetime(*(time.strptime(data.findtext('releasedate').strip(), '%d %b %Y, 00:00')[0:6]))
        self.__image = dict([(i.get('size'), i.text) for i in data.findall('image')])
        self.__stats = Stats(
                       subject = self,
                       listeners = int(data.findtext('listeners')),
                       playcount = int(data.findtext('playcount')),
                       )
        self.__topTags = [
                    Tag(
                        self.__api,
                        name = t.findtext('name'),
                        url = t.findtext('url')
                        ) 
                    for t in data.findall('toptags/tag')
                    ]
                         
    @staticmethod
    def getInfo(api,
                artist = None,
                album = None,
                mbid = None):
        data = Album._fetchData(api, artist, album, mbid)
        a = Album(
                  api,
                  name = data.findtext('name'),
                  artist = Artist(
                                  api,
                                  name = data.findtext('artist'),
                                  ),
                  )
        if a.id is None:
            a._fillInfo()
        return a
        
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash("%s%s" % (kwds['name'], hash(kwds['artist'])))
        except KeyError:
            raise LastfmError("name and artist have to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(name = self.name, artist = self.artist)
        
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
from error import LastfmError
from stats import Stats
from tag import Tag