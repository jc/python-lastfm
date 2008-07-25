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

    def getSubject(self):
        return self.__subject

    def getRank(self):
        return self.__rank

    def getListeners(self):
        return self.__listeners

    def getPlaycount(self):
        return self.__playcount

    def getTagcount(self):
        return self.__tagcount
    
    def getCount(self):
        return self.__count
        
    def getMatch(self):
        return self.__match

    def getWeight(self):
        return self.__weight

    def getAttendance(self):
        return self.__attendance

    def getReviews(self):
        return self.__reviews

    listeners = property(getListeners, None, None, "Listeners's Docstring")

    playcount = property(getPlaycount, None, None, "Plays's Docstring")
    
    tagcount = property(getTagcount, None, None, "Plays's Docstring")
    
    count = property(getCount, None, None, "Plays's Docstring")

    match = property(getMatch, None, None, "Match's Docstring")

    rank = property(getRank, None, None, "Artist's Docstring")

    subject = property(getSubject, None, None, "subject's Docstring")

    weight = property(getWeight, None, None, "Weight's Docstring")

    attendance = property(getAttendance, None, None, "Attendance's Docstring")

    reviews = property(getReviews, None, None, "Reviews's Docstring")

    def __repr__(self):
        return "<lastfm.Stats: for '%s'>" % self.__subject.name
    