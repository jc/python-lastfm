#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Track(object):
    """A class representing a track."""
    def __init__(self,
                 name = None,
                 mbid = None,
                 url = None,
                 streamable = None,
                 artist = None,
                 image = None,
                 match = None):
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