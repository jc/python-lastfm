#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from album import Album
from api import Api
from artist import Artist
from base import LastfmBase
from error import Error
from event import Event
from geo import Location, Country
from group import Group
from playlist import Playlist
from registry import Registry
from tag import Tag
from tasteometer import Tasteometer
from track import Track
from user import User

__all__ = ['Error', 'Api', 'Album', 'Artist', 'Event',
           'Location', 'Country', 'Group', 'Playlist', 'Tag',
           'Tasteometer', 'Track', 'User', 'Registry']