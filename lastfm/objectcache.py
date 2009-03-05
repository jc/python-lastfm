#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from lastfm.album import Album
from lastfm.artist import Artist
from lastfm.mixins import Cacheable
from lastfm.error import InvalidParametersError
from lastfm.event import Event
from lastfm.geo import Location, Country
from lastfm.group import Group
from lastfm.playlist import Playlist
from lastfm.tag import Tag
from lastfm.track import Track
from lastfm.user import User
from lastfm.venue import Venue
from lastfm.weeklychart import WeeklyAlbumChart, WeeklyArtistChart, WeeklyTrackChart

class ObjectCache(object):
    """The registry to contain all the entities"""
    keys = [c.__name__ for c in [Album, Artist, Event, Location, Country, Group, 
            Playlist, Tag, Track, User, Venue, WeeklyAlbumChart, WeeklyArtistChart, WeeklyTrackChart]]
    
    def __getitem__(self, name):
        if name not in ObjectCache.keys:
            raise InvalidParametersError("Key does not correspond to a valid class")
        else:
            try:
                vals = Cacheable.registry[eval(name)].values()
                vals.sort()
                return vals
            except KeyError:
                return []
            
    def __repr__(self):
        return "<lastfm.ObjectCache>"