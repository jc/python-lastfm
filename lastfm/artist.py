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
                 tags = None,
                 bio = None):
        self.__api = api
        self.__name = name
        self.__mbid = mbid
        self.___url = url
        self.__image = image
        self.__streamable = streamable
        self.__stats = stats
        self.__similar = similar
        self.__tags = tags
        self.__bio = bio

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

    def getSimilar(self):
        if self.__similar:
            return self.__similar
        else:
            pass
 
    def getTags(self):
        return self.__tags

    def getBio(self):
        return self.__bio
    
    name = property(getName, None, None, "Name's Docstring")

    mbid = property(getMbid, None, None, "Mbid's Docstring")

    image = property(getImage, None, None, "Image's Docstring")

    streamable = property(getStreamable, None, None, "Streamable's Docstring")

    stats = property(getStats, None, None, "Stats's Docstring")

    similar = property(getSimilar, None, None, "Similar's Docstring")

    tags = property(getTags, None, None, "Tags's Docstring")

    bio = property(getBio, None, None, "Bio's Docstring")        
    
    @staticmethod
    def getInfo(api,
                artist = None,
                mbid = None):
        pass
    
    
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
