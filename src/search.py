#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class SearchResult(object):
    """A class to represent a search result"""
    xmlns = "http://a9.com/-/spec/opensearch/1.1/"
    def __init__(self,
             type = None,
             searchTerms = None,
             startPage = None,
             totalResults = None,
             startIndex = None,
             itemsPerPage = None,
             matches = None):
        self.__type = type
        self.__searchTerms = searchTerms
        self.__startPage = startPage
        self.__totalResults = totalResults
        self.__startIndex = startIndex
        self.__itemsPerPage = itemsPerPage
        self.__matches = matches
    
    @property
    def type(self):
        """type of the search"""
        return self.__type

    @property
    def searchTerms(self):
        """terms searched for in the search"""
        return self.__searchTerms

    @property
    def startPage(self):
        """start page of the search"""
        return self.__startPage

    @property
    def totalResults(self):
        """number of total results for the search"""
        return self.__totalResults

    @property
    def startIndex(self):
        """start index of the search"""
        return self.__startIndex

    @property
    def itemsPerPage(self):
        """number of items per page for the search"""
        return self.__itemsPerPage

    @property
    def matches(self):
        """match result of the search"""
        return self.__matches
    
    @LastfmBase.topProperty("matches")
    def topMatch(self):
        """top match for the search"""
        pass
                
    def __repr__(self):
        return "<lastfm.SearchResult: %s results for %s '%s'>" % (self.totalResults, self.type, self.searchTerms)