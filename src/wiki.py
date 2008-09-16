#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

class Wiki(object):
        """A class representing the information from the wiki of the subject."""
        def __init__(self,
                     subject,
                     published = None,
                     summary = None,
                     content = None):
            self.__subject = subject
            self.__published = published
            self.__summary = summary
            self.__content = content
    
        @property
        def subject(self):
            """artist for which the biography is"""
            return self.__subject
    
        @property
        def published(self):
            """publication time of the biography"""
            return self.__published
    
        @property
        def summary(self):
            """summary of the biography"""
            return self.__summary
    
        @property
        def content(self):
            """content of the biography"""
            return self.__content
    
        def __repr__(self):
            return "<lastfm.Wiki: for %s '%s'>" % (self.subject.__class__.__name__, self.subject.name)