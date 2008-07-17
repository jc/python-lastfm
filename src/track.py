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

    def getName(self):
        return self.__name

    def getMbid(self):
        return self.__mbid

    def getUrl(self):
        return self.__url

    def getStreamable(self):
        return self.__streamable

    def getArtist(self):
        return self.__artist

    def getImage(self):
        return self.__image

    def getStats(self):
        return self.__stats
    
    def getFullTrack(self):
        return self.__fullTrack

    name = property(getName, None, None, "Name's Docstring")

    mbid = property(getMbid, None, None, "Mbid's Docstring")

    url = property(getUrl, None, None, "Url's Docstring")

    streamable = property(getStreamable, None, None, "Streamable's Docstring")

    artist = property(getArtist, None, None, "Artist's Docstring")

    image = property(getImage, None, None, "Image's Docstring")

    stats = property(getStats, None, None, "Match's Docstring")
    
    fullTrack = property(getFullTrack, None, None, "Match's Docstring")
    
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
        data = self.__api.fetchData(params).find('similartracks')
        
    similar = property(getSimilar, None, None, "Similar's Docstring")
    mostSimilar = property(lambda self: len(self.similar) and self.similar[0],
                           None, None, "docstring")
        
    def getTopFans(self,
                   artist = None,
                   track = None,
                   mbid = None):
        params = self.__checkParams({'method': 'track.gettopfans'}, artist, track, mbid)
        data = self.__api.fetchData(params).find('topfans')
        
    topFans = property(getTopFans, None, None, "top fans's Docstring")
    topFan = property(lambda self: len(self.topFans) and self.topFans[0],
                      None, None, "docstring")
        
    def getTopTags(self,
                   artist = None,
                   track = None,
                   mbid = None):
        params = self.__checkParams({'method': 'track.gettoptags'}, artist, track, mbid)
        data = self.__api.fetchData(params).find('toptags')
        
    topTags = property(getTopTags, None, None, "docstring")
    topTag = property(lambda self: len(self.topTags) and self.topTags[0], None, None, "docstring")
    
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