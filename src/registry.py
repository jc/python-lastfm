#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from error import LastfmError

from album import Album
from artist import Artist
from event import Event
from geo import Location, Country
from group import Group
from playlist import Playlist
from tag import Tag
from track import Track
from user import User
from search import SearchResult

class Registry(object):
    """The registry to contain all the entities"""
    keys = [Album, Artist, Event, Location, Country, Group, 
            Playlist, Tag, Track, User, SearchResult]
    
    def get(self, name):
        if name not in Registry.keys:
            raise LastfmError("Key does not correspond to a valid class")
        else:
            try:
                vals = LastfmBase.registry[name].values()
                vals.sort()
                return vals
            except KeyError:
                return []
            
    def __repr__(self):
        return "<lastfm.Registry>"