#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Track(object):
    """A class representing a track."""
    def __init__(self,
                 api,
                 name = None,
                 mbid = None,
                 url = None,
                 streamable = None,
                 artist = None,
                 image = None,
                 match = None):
        self.__api = api
        self.__name = name
        self.__mbid = mbid
        self.__url = url
        self.__streamable = streamable
        self.__artist = artist
        self.__image = image
        self.__match = match

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

    def getMatch(self):
        return self.__match

    name = property(getName, None, None, "Name's Docstring")

    mbid = property(getMbid, None, None, "Mbid's Docstring")

    url = property(getUrl, None, None, "Url's Docstring")

    streamable = property(getStreamable, None, None, "Streamable's Docstring")

    artist = property(getArtist, None, None, "Artist's Docstring")

    image = property(getImage, None, None, "Image's Docstring")

    match = property(getMatch, None, None, "Match's Docstring")
    
    def __checkParams(self,
                      params,
                      artist = None,
                      track = None,
                      mbid = None):
        if not ((artist and track) or mbid):
            raise LastfmError("either (artist and track) or mbid has to be given as argument.")
        
        if artist and album:
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
        
from error import LastfmError
from user import user
from tag import Tag