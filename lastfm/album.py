#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Album(object):
    """A class representing an album."""
    def __init__(self,
                 api,
                 name = None,
                 artist = None,
                 id = None,
                 mbid = None,
                 url = None,
                 releaseDate = None,
                 image = None,
                 listeners = None,
                 playcount = None,
                 topTags = None):
        self.__api = api
        self.__name = name
        self.__artist = artist
        self.__id = id
        self.__mbid = mbid
        self.__url = url
        self.__releaseDate = releaseDate
        self.__image = image
        self.__listeners = listeners
        self.__playcount = playcount
        self.__topTags = topTags

    def getName(self):
        return self.__name
    
    def getArtist(self):
        return self.__artist

    def getId(self):
        return self.__id

    def getMbid(self):
        return self.__mbid

    def getUrl(self):
        return self.__url

    def getReleaseDate(self):
        return self.__releaseDate

    def getImage(self):
        return self.__image

    def getListeners(self):
        return self.__listeners

    def getPlaycount(self):
        return self.__playcount

    def getTopTags(self):
        return self.__topTags

    name = property(getName, None, None, "Name's Docstring")

    artist = property(getArtist, None, None, "Artist's Docstring")

    id = property(getId, None, None, "Id's Docstring")

    mbid = property(getMbid, None, None, "Mbid's Docstring")

    url = property(getUrl, None, None, "Url's Docstring")

    releaseDate = property(getReleaseDate, None, None, "ReleaseDate's Docstring")

    image = property(getImage, None, None, "Image's Docstring")

    listeners = property(getListeners, None, None, "Listeners's Docstring")

    playcount = property(getPlaycount, None, None, "Playcount's Docstring")

    topTags = property(getTopTags, None, None, "TopTags's Docstring")
    
    @staticmethod
    def getInfo(api,
                artist = None,
                album = None,
                mbid = None):
        apiKey = api.getApiKey()
        params = {'method': 'album.getinfo', 'api_key': apiKey}
        if not ((artist and album) or mbid):
            raise LastfmError("either (artist and album) or mbid has to be given as argument.")
        if artist and album:
            params.update({'artist': artist, 'album': album})
        elif mbid:
            params.update({'mbid': mbid})
        xml = api.fetchUrl(Api.API_ROOT_URL, params)
        data = Xml2Dict(ElementTree.XML(xml))
        if data['@status'] != "ok":
            raise LastfmError("Error code: %s (%s)" % (data['error']['@code'], data['error']['text']))
        
        return Album(
                     api,
                     name = data['album']['name'],
                     artist = Artist(
                            api,
                            name = data['album']['artist']
                            ),
                     id = int(data['album']['id']),
                     mbid = data['album']['mbid'],
                     url = data['album']['url'],
                     releaseDate = data['album']['releasedate'] and 
                                        datetime(*(time.strptime(data['album']['releasedate'], '%d %b %Y, 00:00')[0:6])),
                     image = dict([(i['@size'],i['text']) for i in data['album']['image']]),
                     listeners = int(data['album']['listeners']),
                     playcount = int(data['album']['playcount']),
                     topTags = [Tag(api, name = t['name'], url = t['url']) for t in data['album']['toptags']['tag']]
                    )
                     
        
import cElementTree as ElementTree
from datetime import datetime
import time

from xml2dict import Xml2Dict
from error import LastfmError
from api import Api
from tag import Tag
from artist import Artist