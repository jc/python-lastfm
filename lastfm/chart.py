#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm"

from lastfm.base import LastfmBase
from lastfm.mixins import Cacheable
from operator import xor

class Chart(LastfmBase, Cacheable):
    """A class for representing the weekly charts"""

    def init(self, subject, start, end, stats = None):
        self._subject = subject
        self._start = start
        self._end = end
        self._stats = stats

    @property
    def subject(self):
        return self._subject

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end
    
    @property
    def stats(self):
        return self._stats
    
    @staticmethod
    def create_from_data(api, subject, data):
        return Chart(
                     subject = subject,
                     start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                     end = datetime.utcfromtimestamp(int(data.attrib['to']))
                     )
    
    @staticmethod
    def _check_chart_params(params, start = None, end = None):
        if xor(start is None, end is None):
            raise InvalidParametersError("both start and end have to be provided.")
        if start is not None and end is not None:
            if isinstance(start, datetime) and isinstance(end, datetime):
                params.update({
                               'from': int(calendar.timegm(start.timetuple())),
                               'to': int(calendar.timegm(end.timetuple()))
                               })
            else:
                raise InvalidParametersError("start and end must be datetime.datetime instances")
            
        return params
    
    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash("%s%s%s%s" % (
                                      kwds['subject'].__class__.__name__,
                                      kwds['subject'].name,
                                      kwds['start'],
                                      kwds['end']
                               ))
        except KeyError:
            raise InvalidParametersError("subject, start and end have to be provided for hashing")
        
    def __hash__(self):
        return self.__class__._hash_func(
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
    
class WeeklyChart(Chart):
    def init(self, subject, start, end, stats = None):
        super(WeeklyChart, self).init(subject, start, end, stats)

class WeeklyAlbumChart(WeeklyChart):
    """A class for representing the weekly album charts"""
    def init(self, subject, start, end, stats, albums):
        super(WeeklyAlbumChart, self).init(subject, start, end, stats)
        self._albums = albums
        
    @property
    def albums(self):
        return self._albums
    
    @staticmethod
    def create_from_data(api, subject, data):
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
        self._artists = artists
        
    @property
    def artists(self):
        return self._artists
    
    @staticmethod
    def create_from_data(api, subject, data):
        w = WeeklyChart(
                        subject = subject,
                        start = datetime.utcfromtimestamp(int(data.attrib['from'])),
                        end = datetime.utcfromtimestamp(int(data.attrib['to'])),
                        )
        count_attribute = data.find('artist').findtext('playcount') and 'playcount' or 'weight'
        def get_count_attribute(artist):
            return {count_attribute: int(eval(artist.findtext(count_attribute)))}
        def get_count_attribute_sum(artists):
            return {count_attribute: reduce(
                        lambda x, y:(x + int(eval(y.findtext(count_attribute)))), artists, 0
                    )}
            
        return WeeklyArtistChart(
            subject = subject,
            start = datetime.utcfromtimestamp(int(data.attrib['from'])),
            end = datetime.utcfromtimestamp(int(data.attrib['to'])),
            stats = Stats(
                          subject = subject,
                          **get_count_attribute_sum(data.findall('artist'))
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
                                          **get_count_attribute(a)
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
        self._tracks = tracks
        
    @property
    def tracks(self):
        return self._tracks
    
    @staticmethod
    def create_from_data(api, subject, data):
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
        
class WeeklyTagChart(WeeklyChart):
    """A class for representing the weekly tag charts"""
    def init(self, subject, start, end, tags, stats):
        super(WeeklyTagChart, self).init(subject, start, end, stats)
        self._tags = tags
        
    @property
    def tags(self):
        return self._tags
    
    @staticmethod
    def create_from_data(api, subject, start, end):
        w = WeeklyChart(
                        subject = subject,
                        start = start,
                        end = end,
                        )
        max_tag_count = 3
        global_top_tags = api.get_global_top_tags()
        from collections import defaultdict

        wac = subject.get_weekly_artist_chart(start, end)
        all_tags = defaultdict(lambda:0)
        tag_weights = defaultdict(lambda:0)
        total_playcount = 0
        artist_count = 0
        for artist in wac.artists:
            artist_count += 1
            total_playcount += artist.stats.playcount
            tag_count = 0
            for tag in artist.top_tags:
                if tag not in global_top_tags: continue
                if tag_count >= max_tag_count: break
                all_tags[tag] += 1
                tag_count += 1
                
            artist_pp = artist.stats.playcount/float(wac.stats.playcount)
            cumulative_pp = total_playcount/float(wac.stats.playcount)
            if (cumulative_pp > 0.75 or artist_pp < 0.01) and artist_count > 10:
                break
        
        for artist in wac.artists[:artist_count]:
            artist_pp = artist.stats.playcount/float(wac.stats.playcount)
            tf = 1/float(max_tag_count)
            tag_count = 0
            weighted_tfidfs = {}
            for tag in artist.top_tags:
                if tag not in global_top_tags: continue
                if tag_count >= max_tag_count: break            
                
                df = all_tags[tag]/float(artist_count)
                tfidf = tf/df
                weighted_tfidf = float(max_tag_count - tag_count)*tfidf
                weighted_tfidfs[tag.name] = weighted_tfidf
                tag_count += 1
                
            sum_weighted_tfidfs = sum(weighted_tfidfs.values())
            for tag in weighted_tfidfs:
                tag_weights[tag] += weighted_tfidfs[tag]/sum_weighted_tfidfs*artist_pp            
            
            artist_pp = artist.stats.playcount/float(wac.stats.playcount)
                
        tag_weights_sum = sum(tag_weights.values())
        tag_weights = tag_weights.items()
        tag_weights.sort(key=lambda x:x[1], reverse=True)
        for i in xrange(len(tag_weights)):
            tag, weight = tag_weights[i]
            tag_weights[i] = (tag, weight, i+1)
        
        wtc = WeeklyTagChart(
           subject = subject,
           start = wac.start,
           end = wac.end,
           stats = Stats(
                         subject = subject,
                         playcount = 1000
                         ),
           tags = [
                     Tag(
                           api,
                           subject = w,
                           name = tag,
                           stats = Stats(
                                         subject = tag,
                                         rank = rank,
                                         count = int(round(1000*weight/tag_weights_sum)),
                                         )
                           )
                     for (tag, weight, rank) in tag_weights
                     ]
           )
        wtc._artist_spectrum_analyzed = 100*total_playcount/float(wac.stats.playcount)
        return wtc

class RollingChart(Chart):
    pass

class MonthlyChart(RollingChart):
    pass

class MonthlyAlbumChart(MonthlyChart):
    pass

class MonthlyArtistChart(MonthlyChart):
    pass

class MonthlyTrackChart(MonthlyChart):
    pass

class MonthlyTagChart(MonthlyChart):
    pass

class ThreeMonthlyChart(RollingChart):
    pass

class ThreeMonthlyAlbumChart(ThreeMonthlyChart):
    pass

class ThreeMonthlyArtistChart(ThreeMonthlyChart):
    pass

class ThreeMonthlyTrackChart(ThreeMonthlyChart):
    pass

class ThreeMonthlyTagChart(ThreeMonthlyChart):
    pass

class SixMonthlyChart(RollingChart):
    pass

class SixMonthlyAlbumChart(SixMonthlyChart):
    pass

class SixMonthlyArtistChart(SixMonthlyChart):
    pass

class SixMonthlyTrackChart(SixMonthlyChart):
    pass

class SixMonthlyTagChart(SixMonthlyChart):
    pass

class YearlyChart(RollingChart):
    pass

class YearlyAlbumChart(YearlyChart):
    pass

class YearlyArtistChart(YearlyChart):
    pass

class YearlyTrackChart(YearlyChart):
    pass

class YearlyTagChart(YearlyChart):
    pass

__all__ = [
    'WeeklyChart',
    'WeeklyAlbumChart', 'WeeklyArtistChart', 'WeeklyTrackChart', 'WeeklyTagChart',
    'MonthlyChart',
    'MonthlyAlbumChart', 'MonthlyArtistChart', 'MonthlyTrackChart', 'MonthlyTagChart', 
    'ThreeMonthlyChart',
    'ThreeMonthlyAlbumChart', 'ThreeMonthlyArtistChart', 'ThreeMonthlyTrackChart', 'ThreeMonthlyTagChart',
    'SixMonthlyChart',
    'SixMonthlyAlbumChart', 'SixMonthlyArtistChart', 'SixMonthlyTrackChart', 'SixMonthlyTagChart',
    'YearlyChart',
    'YearlyAlbumChart', 'YearlyArtistChart', 'YearlyTrackChart', 'YearlyTagChart'
]
from datetime import datetime
import calendar

from lastfm.album import Album
from lastfm.artist import Artist
from lastfm.error import InvalidParametersError
from lastfm.stats import Stats
from lastfm.track import Track
from lastfm.tag import Tag