#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Track(LastfmBase):
    """A class representing a track."""
    def init(self,
                 api,
                 name = None,
                 mbid = None,
                 url = None,
                 streamable = None,
                 artist = None,
                 image = None,
                 stats = None,
                 fullTrack = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__mbid = mbid
        self.__url = url
        self.__streamable = streamable
        self.__artist = artist
        self.__image = image
        self.__stats = stats and Stats(
                             subject = self,
                             match = stats.match,
                             playcount = stats.playcount,
                             rank = stats.rank
                            )
        self.__fullTrack = fullTrack

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
    def streamable(self):
        """is the track streamable"""
        return self.__streamable

    @property
    def artist(self):
        """artist of the track"""
        return self.__artist

    @property
    def image(self):
        """image of the track's album cover"""
        return self.__image

    @property
    def stats(self):
        """stats of the track"""
        return self.__stats
    
    @property
    def fullTrack(self):
        """is the full track streamable"""
        return self.__fullTrack
    
    def __checkParams(self,
                      params,
                      artist = None,
                      track = None,
                      mbid = None):
        if not ((artist and track) or mbid):
            raise LastfmError("either (artist and track) or mbid has to be given as argument.")
        
        if artist and track:
            params.update({'artist': artist, 'track': track})
        elif mbid:
            params.update({'mbid': mbid})
        return params
        
    def getSimilar(self,
                   artist = None,
                   track = None,
                   mbid = None):
        params = self.__checkParams({'method': 'track.getsimilar'}, artist, track, mbid)
        data = self.__api._fetchData(params).find('similartracks')
        
    @property
    def similar(self):
        """tracks similar to this track"""
        return self.getSimilar()
    
    @property
    def mostSimilar(self):
        """track most similar to this track"""
        return (len(self.similar) and self.similar[0] or None)
        
    def getTopFans(self,
                   artist = None,
                   track = None,
                   mbid = None):
        params = self.__checkParams({'method': 'track.gettopfans'}, artist, track, mbid)
        data = self.__api._fetchData(params).find('topfans')
        
    @property
    def topFans(self):
        """top fans of the track"""
        return self.getTopFans()
    
    @property
    def topFan(self):
        return (len(self.topFans) and self.topFans[0] or None)
        
    def getTopTags(self,
                   artist = None,
                   track = None,
                   mbid = None):
        params = self.__checkParams({'method': 'track.gettoptags'}, artist, track, mbid)
        data = self.__api._fetchData(params).find('toptags')
        
    @property
    def topTags(self):
        """top tags for the track"""
        return self.getTopTags()
    
    @property
    def topTag(self):
        return (len(self.topTags) and self.topTags[0] or None)
    
    @staticmethod
    def search(api,
               track,
               artist = None,
               limit = None,
               page = None):
        pass
    
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash("%s%s" % (kwds['name'], hash(kwds['artist'])))
        except KeyError:
            raise LastfmError("name and artist have to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(name = self.name, artist = self.artist)
    
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

from api import Api
from error import LastfmError
from user import User
from tag import Tag
from stats import Stats