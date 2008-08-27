#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class WeeklyChart(LastfmBase):
    """A class for representing the weekly charts"""

    def init(self, subject, start, end):
        self._subject = subject
        self._start = start
        self._end = end

    @property
    def subject(self):
        return self._subject

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end
    
    @staticmethod
    def createFromData(api, subject, data):
        return WeeklyChart(
                           subject = subject,
                           start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                           end = datetime.utcfromtimestamp(int(data.attrib['to']))
                           )
        
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return "%s%s%s%s" % (
                               hash(kwds['subject'].__class__.__name__),
                               hash(kwds['subject'].name),
                               hash(kwds['start']),
                               hash(kwds['end'])
                               )
        except KeyError:
            raise LastfmError("subject, start and end have to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(
                                       subject = self.subject,
                                       start = self.start,
                                       end = self.end
                                       )
    
    def __eq__(self, other):
        return self.subject == other.subject and \
                self.start == other.start and \
                self.end == other.end
    
    def __lt__(self, other):
        if self.subject == other.subject:
            if self.start == other.start:
                return self.end < other.end
            else:
                return self.start < other.start
        else:
            return self.subject < other.subject
    
    def __repr__(self):
        return "<lastfm.%s: for %s:%s from %s to %s>" % \
            (
             self.__class__.__name__,
             self.subject.__class__.__name__,
             self.subject.name,
             self.start.strftime("%x"),
             self.end.strftime("%x"),
            )
    
class WeeklyAlbumChart(WeeklyChart):
    """A class for representing the weekly album charts"""
    def init(self, subject, start, end, albums):
        self._subject = subject
        self._start = start
        self._end = end
        self.__albums = albums
        
    @property
    def albums(self):
        return self.__albums
    
    @staticmethod
    def createFromData(api, subject, data):
        return WeeklyAlbumChart(
                           subject = subject,
                           start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                           end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                           albums = [
                                     Album(
                                           api,
                                           name = a.findtext('name'),
                                           mbid = a.findtext('mbid'),
                                           artist = Artist(
                                                           api,
                                                           name = a.findtext('artist'),
                                                           mbid = a.find('artist').attrib['mbid'],
                                                           ),
                                           stats = Stats(
                                                         subject = a.findtext('name'),
                                                         rank = int(a.attrib['rank']),
                                                         playcount = int(a.findtext('playcount')),
                                                         ),
                                           url = a.findtext('url'),
                                           )
                                     for a in data.findall('album')
                                     ]
                           )
    
class WeeklyArtistChart(WeeklyChart):
    """A class for representing the weekly artist charts"""
    def init(self, subject, start, end, artists):
        self._subject = subject
        self._start = start
        self._end = end
        self.__artists = artists
        
    @property
    def artists(self):
        return self.__artists
    
    @staticmethod
    def createFromData(api, subject, data):
        return WeeklyArtistChart(
                           subject = subject,
                           start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                           end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                           artists = [
                                     Artist(
                                           api,
                                           name = a.findtext('name'),
                                           mbid = a.findtext('mbid'),
                                           stats = Stats(
                                                         subject = a.findtext('name'),
                                                         rank = int(a.attrib['rank']),
                                                         playcount = int(a.findtext('playcount')),
                                                         ),
                                           url = a.findtext('url'),
                                           )
                                     for a in data.findall('artist')
                                     ]
                           )
    
class WeeklyTrackChart(WeeklyChart):
    """A class for representing the weekly track charts"""
    def init(self, subject, start, end, tracks):
        self._subject = subject
        self._start = start
        self._end = end
        self.__tracks = tracks
        
    @property
    def tracks(self):
        return self.__tracks
    
    @staticmethod
    def createFromData(api, subject, data):
        return WeeklyTrackChart(
                           subject = subject,
                           start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                           end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                           tracks = [
                                     Track(
                                           api,
                                           name = t.findtext('name'),
                                           mbid = t.findtext('mbid'),
                                           artist = Artist(
                                                           api,
                                                           name = t.findtext('artist'),
                                                           mbid = t.find('artist').attrib['mbid'],
                                                           ),
                                           stats = Stats(
                                                         subject = t.findtext('name'),
                                                         rank = int(t.attrib['rank']),
                                                         playcount = int(t.findtext('playcount')),
                                                         ),
                                           url = t.findtext('url'),
                                           )
                                     for t in data.findall('track')
                                     ]
                           )
    
from datetime import datetime

from album import Album
from artist import Artist
from error import LastfmError
from stats import Stats
from track import Track