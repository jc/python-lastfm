#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm"

class Wiki(object):
        """A class representing the information from the wiki of the subject."""
        def __init__(self,
                     subject,
                     published = None,
                     summary = None,
                     content = None):
            self._subject = subject
            self._published = published
            self._summary = summary
            self._content = content
    
        @property
        def subject(self):
            """artist for which the biography is"""
            return self._subject
    
        @property
        def published(self):
            """publication time of the biography"""
            return self._published
    
        @property
        def summary(self):
            """summary of the biography"""
            return self._summary
    
        @property
        def content(self):
            """content of the biography"""
            return self._content
    
        def __repr__(self):
            return "<lastfm.Wiki: for %s '%s'>" % (self.subject.__class__.__name__, self.subject.name)