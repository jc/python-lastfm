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

    @property
    def score(self):
        """score of the comparison"""
        return self.__score

    @property
    def matches(self):
        """matches for the comparison"""
        return self.__matches

    @property
    def artists(self):
        """artists for the comparison"""
        return self.__artists
    
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
        