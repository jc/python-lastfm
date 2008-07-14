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
        params = {'method': 'album.getinfo'}
        if not ((artist and album) or mbid):
            raise LastfmError("either (artist and album) or mbid has to be given as argument.")
        if artist and album:
            params.update({'artist': artist, 'album': album})
        elif mbid:
            params.update({'mbid': mbid})
        data = api.fetchData(params).find('album')

        return Album(
                     api,
                     name = data.findtext('name'),
                     artist = Artist(
                                     api,
                                     name = data.findtext('artist'),
                                     ),
                     id = int(data.findtext('id')),
                     mbid = data.findtext('mbid'),
                     url = data.findtext('url'),
                     releaseDate = data.findtext('releasedate') and 
                                        datetime(*(time.strptime(data.findtext('releasedate').strip(), '%d %b %Y, 00:00')[0:6])),
                     image = dict([(i.get('size'), i.text) for i in data.findall('image')]),
                     listeners = int(data.findtext('listeners')),
                     playcount = int(data.findtext('playcount')),
                     topTags = [
                                Tag(
                                    api,
                                    name = t.findtext('name'),
                                    url = t.findtext('url')
                                    ) 
                                for t in data.findall('toptags/tag')
                                ]
                     )
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
        return "<lastfm.Album: %s by %s>" % (self.name, self.artist.name)
        
                     
from datetime import datetime
import time

from error import LastfmError
from tag import Tag
from artist import Artist