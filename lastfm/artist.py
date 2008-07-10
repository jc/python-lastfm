#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Artist(object):
    """A class representing an artist."""
    def __init__(self,
                 api,
                 name = None,
                 mbid = None,
                 url = None,
                 image = None,
                 streamable = None,
                 stats = None,
                 similar = None,
                 topTags = None,
                 bio = None):
        self.__api = api
        self.__name = name
        self.__mbid = mbid
        self.___url = url
        self.__image = image
        self.__streamable = streamable
        self.__stats = stats and Stats(
                             artist = self,
                             listeners = stats.listeners,
                             plays = stats.plays
                            )
        self.__similar = similar
        self.__topTags = topTags
        self.__bio = bio and Bio(
                         artist = self,
                         published = bio.published,
                         summary = bio.summary,
                         content = bio.content
                        )

    def getName(self):
        return self.__name

    def getMbid(self):
        return self.__mbid

    def getImage(self):
        return self.__image

    def getStreamable(self):
        return self.__streamable

    def getStats(self):
        return self.__stats

    def getSimilar(self, limit = None):
        if self.__similar:
            return self.__similar
        else:
            pass

    def getTopTags(self):
        if self.__topTags:
            return self.__topTags
        else:
            pass

    def getBio(self):
        return self.__bio

    name = property(getName, None, None, "Name's Docstring")

    mbid = property(getMbid, None, None, "Mbid's Docstring")

    image = property(getImage, None, None, "Image's Docstring")

    streamable = property(getStreamable, None, None, "Streamable's Docstring")

    stats = property(getStats, None, None, "Stats's Docstring")

    similar = property(getSimilar, None, None, "Similar's Docstring")

    topTags = property(getTopTags, None, None, "Tags's Docstring")

    bio = property(getBio, None, None, "Bio's Docstring")
    
    def getEvents(self):
        pass
    
    def getTopAlbums(self):
        pass
    
    def getTopFans(self):
        pass
    
    def getTopTracks(self):
        pass
    
    @staticmethod
    def search(api,
               artist,
               limit = None,
               page = None):
        pass

    @staticmethod
    def getInfo(api,
                artist = None,
                mbid = None):
        params = {'method': 'artist.getinfo'}
        if not (artist or mbid):
            raise LastfmError("either artist or mbid has to be given as argument.")
        if artist:
            params.update({'artist': artist})
        elif mbid:
            params.update({'mbid': mbid})
        data = api.fetchData(params).find('artist')
                
        return Artist(
                      api,
                      name = data.findtext('name'),
                      mbid = data.findtext('mbid'),
                      url = data.findtext('url'),
                      image = dict([(i.get('size'), i.text) for i in data.findall('image')]),
                      streamable = (data.findtext('streamable') == 1),
                      stats = Stats(
                                    artist,
                                    listeners = int(data.findtext('stats/listeners')),
                                    plays = int(data.findtext('stats/plays'))
                                    ),
                      similar = [
                                 Artist(
                                        api,
                                        name = a.findtext('name'),
                                        url = a.findtext('url'),
                                        image = dict([(i.get('size'), i.text) for i in a.findall('image')])
                                        )
                                 for a in data.findall('similar/artist')
                                 ],
                      tags = [
                              Tag(
                                  api,
                                  name = t.findtext('name'),
                                  url = t.findtext('url')
                                  ) 
                              for t in data.findall('tags/tag')
                              ],
                      bio = Bio(
                                artist,
                                published = datetime(*(time.strptime(
                                                                     data.findtext('bio/published').strip(),
                                                                     '%a, %d %b %Y %H:%M:%S +0000'
                                                                     )[0:6])),
                                summary = data.findtext('bio/summary'),
                                content = data.findtext('bio/content')
                                )
                      )
    
    def __eq__(self, other):
        return self.name == other.name

class Stats(object):
    """A class representing the stats of an artist."""
    def __init__(self,
                 artist,
                 listeners = None,
                 plays = None):
        self.__artist = artist
        self.__listeners = listeners
        self.__plays = plays

    def getArtist(self):
        return self.__artist

    def getListeners(self):
        return self.__listeners

    def getPlays(self):
        return self.__plays

    listeners = property(getListeners, None, None, "Listeners's Docstring")

    plays = property(getPlays, None, None, "Plays's Docstring")

    artist = property(getArtist, None, None, "Artist's Docstring")

class Bio(object):
    """A class representing the biography of an artist."""
    def __init__(self,
                 artist,
                 published = None,
                 summary = None,
                 content = None):
        self.__artist = artist
        self.__published = published
        self.__summary = summary
        self.__content = content

    def getArtist(self):
        return self.__artist

    def getPublished(self):
        return self.__published

    def getSummary(self):
        return self.__summary

    def getContent(self):
        return self.__content

    published = property(getPublished, None, None, "Published's Docstring")

    summary = property(getSummary, None, None, "Summary's Docstring")

    content = property(getContent, None, None, "Content's Docstring")

    artist = property(getArtist, None, None, "Artist's Docstring")

from datetime import datetime
import time
import types

from error import LastfmError
from tag import Tag
