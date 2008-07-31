#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class SearchResult(LastfmBase):
    """A class to represent a search result"""
    xmlns = "http://a9.com/-/spec/opensearch/1.1/"
    def init(self,
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
    
    @property
    def topMatch(self):
        return (len(self.matches) and self.matches[0] or None)
        
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash("%s%s%s" % (kwds['searchTerms'], kwds['type'], kwds['startPage']))
        except KeyError:
            raise LastfmError("searchTerms, type and startPage have to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(
                                       searchTerms = self.searchTerms,
                                       type = self.type,
                                       startPage = self.startPage
                                       )
    
    def __eq__(self, other):
        return (
                self.searchTerms == other.searchTerms and
                self.type == other.type and
                self.startIndex == other.startIndex
                )
    
    def __lt__(self, other):
        if self.searchTerms != other.searchTerms:
            return self.searchTerms < other.searchTerms
        else:
            return self.startIndex < other.startIndex
    
    def __repr__(self):
        return "<lastfm.SearchResult: for %s '%s'>" % (self.type, self.searchTerms)
    
from error import LastfmError