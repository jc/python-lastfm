#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Stats(object):
    """A class representing the stats of an artist."""
    def __init__(self,
                 subject,
                 listeners = None,
                 playcount = None,
                 tagcount = None,
                 count = None,
                 match = None,
                 rank = None,
                 weight = None,
                 attendance = None,
                 reviews = None,):
        self.__subject = subject
        self.__listeners = listeners
        self.__playcount = playcount
        self.__tagcount = tagcount
        self.__count = count
        self.__match = match
        self.__rank = rank
        self.__weight = weight
        self.__attendance = attendance
        self.__reviews = reviews

    @property
    def subject(self):
        """subject of the stats"""
        return self.__subject

    @property
    def rank(self):
        """rank of the subject"""
        return self.__rank

    @property
    def listeners(self):
        """number of listeners of the subject"""
        return self.__listeners

    @property
    def playcount(self):
        """playcount of the subject"""
        return self.__playcount

    @property
    def tagcount(self):
        """tagcount of the subject"""
        return self.__tagcount
    
    @property
    def count(self):
        """count of the subject"""
        return self.__count
        
    @property
    def match(self):
        """match of the subject"""
        return self.__match

    @property
    def weight(self):
        """weight of the subject"""
        return self.__weight

    @property
    def attendance(self):
        """attendance of the subject"""
        return self.__attendance

    @property
    def reviews(self):
        """reviews of the subject"""
        return self.__reviews

    def __repr__(self):
        return "<lastfm.Stats: for '%s'>" % self.__subject.name
    