#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class WeeklyChart(LastfmBase):
    """A class for representing the weekly charts"""

    def init(self, subject, start, end,
             stats = None):
        self.__subject = subject
        self.__start = start
        self.__end = end
        self.__stats = stats

    @property
    def subject(self):
        return self.__subject

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end
    
    @property
    def stats(self):
        return self.__stats
    
    @staticmethod
    def createFromData(api, subject, data):
        return WeeklyChart(
                           subject = subject,
                           start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                           end = datetime.utcfromtimestamp(int(data.attrib['to']))
                           )
    
    @staticmethod
    def _checkWeeklyChartParams(params, start = None, end = None):
        if (start is not None and end is None) or (start is None and end is not None):
            raise LastfmError("both start and end have to be provided.")
        if start is not None and end is not None:
            if isinstance(start, datetime) and isinstance(end, datetime):
                params.update({
                               'from': int(calendar.timegm(start.timetuple())),
                               'to': int(calendar.timegm(end.timetuple()))
                               })
            else:
                raise LastfmError("start and end must be datetime.datetime instances")
            
        return params
    
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash("%s%s%s%s" % (
                                      kwds['subject'].__class__.__name__,
                                      kwds['subject'].name,
                                      kwds['start'],
                                      kwds['end']
                               ))
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
    def init(self, subject, start, end, stats, albums):
        super(WeeklyAlbumChart, self).init(subject, start, end, stats)
        self.__albums = albums
        
    @property
    def albums(self):
        return self.__albums
    
    @staticmethod
    def createFromData(api, subject, data):
        w = WeeklyChart(
                        subject = subject,
                        start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                        end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                        )
        return WeeklyAlbumChart(
                           subject = subject,
                           start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                           end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                           stats = Stats(
                                         subject = subject,
                                         playcount = reduce(
                                                            lambda x,y:(
                                                                        x + int(y.findtext('playcount'))
                                                                        ),
                                                            data.findall('album'),
                                                            0
                                          )
                                    ),
                           albums = [
                                     Album(
                                           api,
                                           subject = w,
                                           name = a.findtext('name'),
                                           mbid = a.findtext('mbid'),
                                           artist = Artist(
                                                           api,
                                                           subject = w,
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
    def init(self, subject, start, end, stats, artists):
        super(WeeklyArtistChart, self).init(subject, start, end, stats)
        self.__artists = artists
        
    @property
    def artists(self):
        return self.__artists
    
    @staticmethod
    def createFromData(api, subject, data):
        w = WeeklyChart(
                        subject = subject,
                        start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                        end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                        )
        return WeeklyArtistChart(
                           subject = subject,
                           start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                           end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                           stats = Stats(
                                         subject = subject,
                                         playcount = reduce(
                                                            lambda x,y:(
                                                                        x + int(y.findtext('playcount'))
                                                                        ),
                                                            data.findall('artist'),
                                                            0
                                          )
                                    ),
                           artists = [
                                     Artist(
                                           api,
                                           subject = w,
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
    def init(self, subject, start, end, tracks, stats):
        super(WeeklyTrackChart, self).init(subject, start, end, stats)
        self.__tracks = tracks
        
    @property
    def tracks(self):
        return self.__tracks
    
    @staticmethod
    def createFromData(api, subject, data):
        w = WeeklyChart(
                        subject = subject,
                        start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                        end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                        )
        return WeeklyTrackChart(
                           subject = subject,
                           start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                           end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                           stats = Stats(
                                         subject = subject,
                                         playcount = reduce(
                                                            lambda x,y:(
                                                                        x + int(y.findtext('playcount'))
                                                                        ),
                                                            data.findall('track'),
                                                            0
                                          )
                                    ),
                           tracks = [
                                     Track(
                                           api,
                                           subject = w,
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
import calendar

from album import Album
from artist import Artist
from error import LastfmError
from stats import Stats
from track import Track