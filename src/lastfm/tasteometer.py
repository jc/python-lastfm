#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Tasteometer(object):
    """A class representing a tasteometer."""
    def __init__(self,
                 score = None,
                 matches = None,
                 artists = None):
        self.__score = score
        self.__matches = matches
        self.__artists = artists#set

    def getScore(self):
        return self.__score

    def getMatches(self):
        return self.__matches

    def getArtists(self):
        return self.__artists

    score = property(getScore, None, None, "Score's Docstring")

    matches = property(getMatches, None, None, "Matches's Docstring")

    artists = property(getArtists, None, None, "Artists's Docstring")
    
    @staticmethod
    def compare(api,
                type1, type2,
                value1, value2,
                limit = None):
        pass
    
    def __repr__(self):
        return "<lastfm.Tasteometer>"
        
from artist import Artist
from error import LastfmError
        