#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
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
        self._subject = subject
        self._listeners = listeners
        self._playcount = playcount
        self._tagcount = tagcount
        self._count = count
        self._match = match
        self._rank = rank
        self._weight = weight
        self._attendance = attendance
        self._reviews = reviews

    @property
    def subject(self):
        """subject of the stats"""
        return self._subject

    @property
    def rank(self):
        """rank of the subject"""
        return self._rank

    @property
    def listeners(self):
        """number of listeners of the subject"""
        return self._listeners

    @property
    def playcount(self):
        """playcount of the subject"""
        return self._playcount

    @property
    def tagcount(self):
        """tagcount of the subject"""
        return self._tagcount
    
    @property
    def count(self):
        """count of the subject"""
        return self._count
        
    @property
    def match(self):
        """match of the subject"""
        return self._match

    @property
    def weight(self):
        """weight of the subject"""
        return self._weight

    @property
    def attendance(self):
        """attendance of the subject"""
        return self._attendance

    @property
    def reviews(self):
        """reviews of the subject"""
        return self._reviews

    def __repr__(self):
        if hasattr(self._subject, 'name'):
            return "<lastfm.Stats: for '%s'>" % self._subject.name
        else:
            return "<lastfm.Stats: for '%s'>" % self._subject
    