#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from album import Album
from artist import Artist
from base import LastfmBase
from error import InvalidParametersError
from event import Event
from geo import Location, Country
from group import Group
from playlist import Playlist
from tag import Tag
from track import Track
from user import User
from weeklychart import WeeklyAlbumChart, WeeklyArtistChart, WeeklyTrackChart

class Registry(object):
    """The registry to contain all the entities"""
    keys = [c.__name__ for c in [Album, Artist, Event, Location, Country, Group, 
            Playlist, Tag, Track, User, WeeklyAlbumChart, WeeklyArtistChart, WeeklyTrackChart]]
    
    def __getitem__(self, name):
        if name not in Registry.keys:
            raise InvalidParametersError("Key does not correspond to a valid class")
        else:
            try:
                vals = LastfmBase.registry[eval(name)].values()
                vals.sort()
                return vals
            except KeyError:
                return []
            
    def __repr__(self):
        return "<lastfm.Registry>"