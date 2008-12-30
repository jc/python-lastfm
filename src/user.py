#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from lazylist import lazylist
import playlist

class User(LastfmBase):
    """A class representing an user."""
    def init(self,
                 api,
                 name = None,
                 url = None,
                 image = None,
                 stats = None,
                 language = None,
                 country = None,
                 age = None,
                 gender = None,
                 subscriber = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__url = url
        self.__image = image
        self.__stats = stats and Stats(
                             subject = self,
                             match = stats.match,
                             weight = stats.weight,
                             playcount = stats.playcount
                            )
        self.__library = User.Library(api, self)
        self.__language = language
        self.__country = country
        self.__age = age
        self.__gender = gender
        self.__subscriber = subscriber

    @property
    def name(self):
        """name of the user"""
        return self.__name

    @property
    def url(self):
        """url of the user's page"""
        return self.__url

    @property
    def image(self):
        """image of the user"""
        return self.__image

    @property
    def stats(self):
        """stats for the user"""
        return self.__stats
    
    @property
    def language(self):
        """lang for the user"""
        return self.__language
    
    @property
    def country(self):
        """country for the user"""
        return self.__country
    
    @property
    def age(self):
        """age for the user"""
        return self.__age
    
    @property
    def gender(self):
        """stats for the user"""
        return self.__gender
    
    @property
    def subscriber(self):
        """is the user a subscriber"""
        return self.__subscriber

    @LastfmBase.cachedProperty
    def events(self):
        params = {'method': 'user.getEvents', 'user': self.name}
        data = self.__api._fetch_data(params).find('events')

        return [
                Event.create_from_data(self.__api, e)
                for e in data.findall('event')
                ]
        
    def get_past_events(self,
                      limit = None):
        params = {'method': 'user.getPastEvents', 'user': self.name}
        if limit is not None:
            params.update({'limit': limit})
                
        @lazylist
        def gen(lst):
            data = self.__api._fetch_data(params).find('events')
            totalPages = int(data.attrib['totalPages'])
            
            @lazylist
            def gen2(lst, data):
                for e in data.findall('event'):
                    yield Event.create_from_data(self.__api, e)
            
            for e in gen2(data):
                yield e
            
            for page in xrange(2, totalPages+1):
                params.update({'page': page})
                data = self.__api._fetch_data(params).find('events')
                for e in gen2(data):
                    yield e            
        return gen()
        
    @LastfmBase.cachedProperty
    def past_events(self):
        return self.get_past_events()

    def get_friends(self,
                   limit = None):
        params = {'method': 'user.getFriends', 'user': self.name}
        if limit is not None:
            params.update({'limit': limit})
        data = self.__api._fetch_data(params).find('friends')
        return [
            User(
                self.__api,
                subject = self,
                name = u.findtext('name'),
                image = dict([(i.get('size'), i.text) for i in u.findall('image')]),
                url = u.findtext('url'),
            )
            for u in data.findall('user')
        ]


    @LastfmBase.cachedProperty
    def friends(self):
        """friends of the user"""
        return self.get_friends()
        
    def get_neighbours(self, limit = None):
        params = {'method': 'user.getNeighbours', 'user': self.name}
        if limit is not None:
            params.update({'limit': limit})
        data = self.__api._fetch_data(params).find('neighbours')
        return [
                User(
                    self.__api,
                    subject = self,
                    name = u.findtext('name'),
                    image = {'medium': u.findtext('image')},
                    url = u.findtext('url'),
                    stats = Stats(
                                  subject = u.findtext('name'),
                                  match = u.findtext('match') and float(u.findtext('match')),
                                  ),
                )
                for u in data.findall('user')
            ]

    @LastfmBase.cachedProperty
    def neighbours(self):
        """neighbours of the user"""
        return self.get_neighbours()
    
    @LastfmBase.topProperty("neighbours")
    def nearest_neighbour(self):
        """nearest neightbour of the user"""
        pass
    
    @LastfmBase.cachedProperty
    def playlists(self):
        """playlists of the user"""
        params = {'method': 'user.getPlaylists', 'user': self.name}
        data = self.__api._fetch_data(params).find('playlists')
        return [
                User.Playlist(
                              self.__api,
                              id = int(p.findtext('id')),
                              title = p.findtext('title'),
                              date = datetime(*(
                                                time.strptime(
                                                              p.findtext('date').strip(),
                                                              '%Y-%m-%dT%H:%M:%S'
                                                              )[0:6])
                              ),
                              size = int(p.findtext('size')),
                              creator = self
                              )
                for p in data.findall('playlist')
                ]

    @LastfmBase.cachedProperty
    def loved_tracks(self):
        params = {'method': 'user.getLovedTracks', 'user': self.name}
        data = self.__api._fetch_data(params).find('lovedtracks')
        return [
                Track(
                    self.__api,
                    subject = self,
                    name = t.findtext('name'),
                    artist = Artist(
                        self.__api,
                        subject = self,
                        name = t.findtext('artist/name'),
                        mbid = t.findtext('artist/mbid'),
                        url = t.findtext('artist/url'),
                    ),
                    mbid = t.findtext('mbid'),
                    image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                    lovedOn = datetime(*(
                        time.strptime(
                            t.findtext('date').strip(),
                            '%d %b %Y, %H:%M'
                            )[0:6])
                        )
                    )
                for t in data.findall('track')
                ]
        
    def get_recent_tracks(self, limit = None):
        params = {'method': 'user.getRecentTracks', 'user': self.name}
        data = self.__api._fetch_data(params, no_cache = True).find('recenttracks')
        return [
                Track(
                      self.__api,
                      subject = self,
                      name = t.findtext('name'),
                      artist = Artist(
                                      self.__api,
                                      subject = self,
                                      name = t.findtext('artist'),
                                      mbid = t.find('artist').attrib['mbid'],
                                      ),
                      album = Album(
                                    self.__api,
                                    subject = self,
                                    name = t.findtext('album'),
                                    artist = Artist(
                                                    self.__api,
                                                    subject = self,
                                                    name = t.findtext('artist'),
                                                    mbid = t.find('artist').attrib['mbid'],
                                                    ),
                                    mbid = t.find('album').attrib['mbid'],
                                    ),
                      mbid = t.findtext('mbid'),
                      streamable = (t.findtext('streamable') == '1'),
                      url = t.findtext('url'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      playedOn = datetime(*(
                                           time.strptime(
                                                         t.findtext('date').strip(),
                                                         '%d %b %Y, %H:%M'
                                                         )[0:6])
                                           )
                      )
                      for t in data.findall('track')
                      ]

    @property
    def recent_tracks(self):
        """recent tracks played by the user"""
        return self.get_recent_tracks()

    @LastfmBase.topProperty("recent_tracks")
    def most_recent_track(self):
        """most recent track played by the user"""
        pass

    def get_top_albums(self, period = None):
        params = {'method': 'user.getTopAlbums', 'user': self.name}
        if period is not None:
            params.update({'period': period})
        data = self.__api._fetch_data(params).find('topalbums')

        return [
                Album(
                     self.__api,
                     subject = self,
                     name = a.findtext('name'),
                     artist = Artist(
                                     self.__api,
                                     subject = self,
                                     name = a.findtext('artist/name'),
                                     mbid = a.findtext('artist/mbid'),
                                     url = a.findtext('artist/url'),
                                     ),
                     mbid = a.findtext('mbid'),
                     url = a.findtext('url'),
                     image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                     stats = Stats(
                                   subject = a.findtext('name'),
                                   playcount = int(a.findtext('playcount')),
                                   rank = int(a.attrib['rank'])
                                   )
                     )
                for a in data.findall('album')
                ]

    @LastfmBase.cachedProperty
    def top_albums(self):
        """overall top albums of the user"""
        return self.get_top_albums()
        
    @LastfmBase.topProperty("top_albums")
    def top_album(self):
        """overall top most album of the user"""
        pass

    def get_top_artists(self, period = None):
        params = {'method': 'user.getTopArtists', 'user': self.name}
        if period is not None:
            params.update({'period': period})
        data = self.__api._fetch_data(params).find('topartists')
        
        return [
                Artist(
                       self.__api,
                       subject = self,
                       name = a.findtext('name'),
                       mbid = a.findtext('mbid'),
                       stats = Stats(
                                     subject = a.findtext('name'),
                                     rank = a.attrib['rank'].strip() and int(a.attrib['rank']) or None,
                                     playcount = a.findtext('playcount') and int(a.findtext('playcount')) or None
                                     ),
                       url = a.findtext('url'),
                       streamable = (a.findtext('streamable') == "1"),
                       image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                       )
                for a in data.findall('artist')
                ]

    @LastfmBase.cachedProperty
    def top_artists(self):
        """top artists of the user"""
        return self.get_top_artists()
        
    @LastfmBase.topProperty("top_artists")
    def top_artist(self):
        """top artist of the user"""
        pass

    def get_top_tracks(self, period = None):
        params = {'method': 'user.getTopTracks', 'user': self.name}
        if period is not None:
            params.update({'period': period})
        data = self.__api._fetch_data(params).find('toptracks')
        return [
                Track(
                      self.__api,
                      subject = self,
                      name = t.findtext('name'),
                      artist = Artist(
                                      self.__api,
                                      subject = self,
                                      name = t.findtext('artist/name'),
                                      mbid = t.findtext('artist/mbid'),
                                      url = t.findtext('artist/url'),
                                      ),
                      mbid = t.findtext('mbid'),
                      stats = Stats(
                                    subject = t.findtext('name'),
                                    rank = t.attrib['rank'].strip() and int(t.attrib['rank']) or None,
                                    playcount = t.findtext('playcount') and int(t.findtext('playcount')) or None
                                    ),
                      streamable = (t.findtext('streamable') == '1'),
                      fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      )
                for t in data.findall('track')
                ]

    @LastfmBase.cachedProperty
    def top_tracks(self):
        """top tracks of the user"""
        return self.get_top_tracks()
        
    @LastfmBase.topProperty("top_tracks")
    def top_track(self):
        """top track of the user"""
        return (len(self.top_tracks) and self.top_tracks[0] or None)

    def get_top_tags(self, limit = None):
        params = {'method': 'user.getTopTags', 'user': self.name}
        if limit is not None:
            params.update({'limit': limit})
        data = self.__api._fetch_data(params).find('toptags')
        return [
                Tag(
                    self.__api,
                    subject = self,
                    name = t.findtext('name'),
                    url = t.findtext('url'),
                    stats = Stats(
                                  subject = t.findtext('name'),
                                  count = int(t.findtext('count'))
                                  )
                    ) 
                for t in data.findall('tag')
                ]

    @LastfmBase.cachedProperty
    def top_tags(self):
        """top tags of the user"""
        return self.get_top_tags()
        
    @LastfmBase.topProperty("top_tags")
    def top_tag(self):
        """top tag of the user"""
        pass

    @LastfmBase.cachedProperty
    def weekly_chart_list(self):
        params = {'method': 'user.getWeeklyChartList', 'user': self.name}
        data = self.__api._fetch_data(params).find('weeklychartlist')
        return [
                WeeklyChart.create_from_data(self.__api, self, c)
                for c in data.findall('chart')
                ]
            
    def get_weekly_album_chart(self,
                             start = None,
                             end = None):
        params = {'method': 'user.getWeeklyAlbumChart', 'user': self.name}
        params = WeeklyChart._check_weekly_chart_params(params, start, end)            
        data = self.__api._fetch_data(params).find('weeklyalbumchart')   
        return WeeklyAlbumChart.create_from_data(self.__api, self, data)

    @LastfmBase.cachedProperty
    def recent_weekly_album_chart(self):
        return self.get_weekly_album_chart()
    
    @LastfmBase.cachedProperty
    def weekly_album_chart_list(self):
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                try:
                    yield self.get_weekly_album_chart(wc.start, wc.end)
                except Error:
                    pass
        return gen()

    def get_weekly_artist_chart(self,
                             start = None,
                             end = None):
        params = {'method': 'user.getWeeklyArtistChart', 'user': self.name}
        params = WeeklyChart._check_weekly_chart_params(params, start, end)
        data = self.__api._fetch_data(params).find('weeklyartistchart')   
        return WeeklyArtistChart.create_from_data(self.__api, self, data)

    @LastfmBase.cachedProperty
    def recent_weekly_artist_chart(self):
        return self.get_weekly_artist_chart()
    
    @LastfmBase.cachedProperty
    def weekly_artist_chart_list(self):
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                try:
                    yield self.get_weekly_artist_chart(wc.start, wc.end)
                except Error:
                    pass
        return gen()

    def get_weekly_track_chart(self,
                             start = None,
                             end = None):
        params = {'method': 'user.getWeeklyTrackChart', 'user': self.name}
        params = WeeklyChart._check_weekly_chart_params(params, start, end)
        data = self.__api._fetch_data(params).find('weeklytrackchart')   
        return WeeklyTrackChart.create_from_data(self.__api, self, data)

    @LastfmBase.cachedProperty
    def recent_weekly_track_chart(self):
        return self.get_weekly_track_chart()
    
    @LastfmBase.cachedProperty
    def weekly_track_chart_list(self):
        wcl = list(self.weekly_chart_list)
        wcl.reverse()
        @lazylist
        def gen(lst):
            for wc in wcl:
                try:
                    yield self.get_weekly_track_chart(wc.start, wc.end)
                except Error:
                    pass
        return gen()
    
    def compare(self, other, limit = None):
        return Tasteometer.compare(self.__api,
                                   'user', 'user',
                                   self.name, other.name,
                                   limit)
    @property
    def library(self):
        return self.__library
    
    @staticmethod
    def get_authenticated_user(api):
        data = api._fetch_data({'method': 'user.getInfo'}, sign = True, session = True).find('user')
        return User(
                api,
                name = data.findtext('name'),
                url = data.findtext('url'),
                language = data.findtext('lang'),
                country = Country(api, name = data.findtext('country')),
                age = int(data.findtext('age')),
                gender = data.findtext('gender'),
                subscriber = (data.findtext('subscriber') == '1'),
                stats = Stats(
                              subject = data.findtext('name'),
                              playcount = data.findtext('playcount')
                              )
            )

    @staticmethod
    def hash_func(*args, **kwds):
        try:
            return hash(kwds['name'])
        except KeyError:
            raise InvalidParametersError("name has to be provided for hashing")

    def __hash__(self):
        return self.__class__.hash_func(name = self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.User: %s>" % self.name
    
    class Playlist(playlist.Playlist):
        """A class representing a playlist belonging to the user."""
        def init(self, api, id, title, date, size, creator):
            super(User.Playlist, self).init(api, "lastfm://playlist/%s" % id)
            self.__id = id
            self.__title = title
            self.__date = date
            self.__size = size
            self.__creator = creator
            
        @property
        def id(self):
            return self.__id
    
        @property
        def title(self):
            return self.__title
    
        @property
        def date(self):
            return self.__date
    
        @property
        def size(self):
            return self.__size
    
        @property
        def creator(self):
            return self.__creator
        
        def addTrack(self, track):
            params = {'method': 'playlist.addTrack', 'playlistID': self.id}
            if not isinstance(track, Track):
                track = self.__api.search_track(track)[0]
            
            params['artist'] = track.artist.name
            params['track'] = track.name
            self.__api._post_data(params)            
        
        @staticmethod
        def hash_func(*args, **kwds):
            try:
                return hash(kwds['id'])
            except KeyError:
                raise InvalidParametersError("id has to be provided for hashing")
            
        def __hash__(self):
            return self.__class__.hash_func(id = self.id)
        
        def __repr__(self):
            return "<lastfm.User.Playlist: %s>" % self.title
        
    class Library(object):
        """A class representing the music library of the user."""
        def __init__(self, api, user):
            self.__api = api
            self.__user = user
            
        @property
        def user(self):
            return self.__user
            
        def get_albums(self,
                      limit = None):
            params = {'method': 'library.getAlbums', 'user': self.user.name}
            if limit is not None:
                params.update({'limit': limit})
            
            @lazylist
            def gen(lst):
                data = self.__api._fetch_data(params).find('albums')
                total_pages = int(data.attrib['totalPages'])
                
                @lazylist
                def gen2(lst, data):
                    for a in data.findall('album'):
                        yield Album(
                                    self.__api,
                                    subject = self,
                                    name = a.findtext('name'),
                                    artist = Artist(
                                                    self.__api,
                                                    subject = self,
                                                    name = a.findtext('artist/name'),
                                                    mbid = a.findtext('artist/mbid'),
                                                    url = a.findtext('artist/url'),
                                                    ),
                                    mbid = a.findtext('mbid'),
                                    url = a.findtext('url'),
                                    image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                                    stats = Stats(
                                                  subject = a.findtext('name'),
                                                  playcount = int(a.findtext('playcount')),
                                                  )
                                    )
                               
                
                for a in gen2(data):
                    yield a
                
                for page in xrange(2, total_pages+1):
                    params.update({'page': page})
                    try:
                        data = self.__api._fetch_data(params).find('albums')
                    except Error:
                        continue
                    for a in gen2(data):
                        yield a            
            return gen()
            
        @LastfmBase.cachedProperty
        def albums(self):
            return self.get_albums()

        def get_artists(self,
                       limit = None):
            params = {'method': 'library.getArtists', 'user': self.user.name}
            if limit is not None:
                params.update({'limit': limit})
            
            @lazylist
            def gen(lst):
                data = self.__api._fetch_data(params).find('artists')
                total_pages = int(data.attrib['totalPages'])
                
                @lazylist
                def gen2(lst, data):
                    for a in data.findall('artist'):
                        yield Artist(
                                     self.__api,
                                     subject = self,
                                     name = a.findtext('name'),
                                     mbid = a.findtext('mbid'),
                                     stats = Stats(
                                                   subject = a.findtext('name'),
                                                   playcount = a.findtext('playcount') and int(a.findtext('playcount')) or None,
                                                   tagcount = a.findtext('tagcount') and int(a.findtext('tagcount')) or None
                                                   ),
                                     url = a.findtext('url'),
                                     streamable = (a.findtext('streamable') == "1"),
                                     image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                                     )                               
                
                for a in gen2(data):
                    yield a
                
                for page in xrange(2, total_pages+1):
                    params.update({'page': page})
                    try:
                        data = self.__api._fetch_data(params).find('artists')
                    except Error:
                        continue
                    for a in gen2(data):
                        yield a            
            return gen()
            
        @LastfmBase.cachedProperty
        def artists(self):
            return self.get_artists()
        
        def get_tracks(self,
                      limit = None):
            params = {'method': 'library.getTracks', 'user': self.user.name}
            if limit is not None:
                params.update({'limit': limit})
            
            @lazylist
            def gen(lst):
                data = self.__api._fetch_data(params).find('tracks')
                totalPages = int(data.attrib['totalPages'])
                
                @lazylist
                def gen2(lst, data):
                    for t in data.findall('track'):
                        yield Track(
                                    self.__api,
                                    subject = self,
                                    name = t.findtext('name'),
                                    artist = Artist(
                                                    self.__api,
                                                    subject = self,
                                                    name = t.findtext('artist/name'),
                                                    mbid = t.findtext('artist/mbid'),
                                                    url = t.findtext('artist/url'),
                                                    ),
                                    mbid = t.findtext('mbid'),
                                    stats = Stats(
                                                  subject = t.findtext('name'),
                                                  playcount = t.findtext('playcount') and int(t.findtext('playcount')) or None,
                                                  tagcount = t.findtext('tagcount') and int(t.findtext('tagcount')) or None
                                                  ),
                                    streamable = (t.findtext('streamable') == '1'),
                                    fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                                    image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                                    )                            
                
                for t in gen2(data):
                    yield t
                
                for page in xrange(2, totalPages+1):
                    params.update({'page': page})
                    data = None
                    try:
                        data = self.__api._fetch_data(params).find('tracks')
                    except Error:
                        continue
                    for t in gen2(data):
                        yield t            
            return gen()
        
        @LastfmBase.cachedProperty
        def tracks(self):
            return self.get_tracks()
        
        @staticmethod
        def hash_func(*args, **kwds):
            try:
                return hash(kwds['user'])
            except KeyError:
                raise InvalidParametersError("user has to be provided for hashing")
    
        def __hash__(self):
            return self.__class__.hash_func(user = self.user)
            
        def __repr__(self):
            return "<lastfm.User.Library: for user '%s'>" % self.user.name

from datetime import datetime
import time

from api import Api
from artist import Artist
from album import Album
from error import Error, InvalidParametersError
from event import Event
from geo import Country
from stats import Stats
from tag import Tag
from tasteometer import Tasteometer
from track import Track
from weeklychart import WeeklyChart, WeeklyAlbumChart, WeeklyArtistChart, WeeklyTrackChart