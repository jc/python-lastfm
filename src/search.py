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
    
    def getType(self):
        return self.__type

    def getSearchTerms(self):
        return self.__searchTerms

    def getStartPage(self):
        return self.__startPage

    def getTotalResults(self):
        return self.__totalResults

    def getStartIndex(self):
        return self.__startIndex

    def getItemsPerPage(self):
        return self.__itemsPerPage

    def getMatches(self):
        return self.__matches
    
    type = property(getType, None, None, "Type's Docstring")

    searchTerms = property(getSearchTerms, None, None, "SearchTerm's Docstring")

    startPage = property(getStartPage, None, None, "StartPage's Docstring")

    totalResults = property(getTotalResults, None, None, "TotalResults's Docstring")

    startIndex = property(getStartIndex, None, None, "StartIndex's Docstring")

    itemsPerPage = property(getItemsPerPage, None, None, "ItemsPerPage's Docstring")

    matches = property(getMatches, None, None, "Matches's Docstring")
    topMatch = property(lambda self: len(self.matches) and self.matches[0],
                        None, None, "docstring")
        
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