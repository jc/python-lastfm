#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from sharable import Sharable

class Event(LastfmBase, Sharable):
    """A class representing an event."""
    STATUS_ATTENDING = 0
    STATUS_MAYBE = 1
    STATUS_NOT = 2
    
    def init(self,
                 api,
                 id = None,
                 title = None,
                 artists = None,
                 headliner = None,
                 venue = None,
                 start_date = None,
                 description = None,
                 image = None,
                 url = None,
                 stats = None,
                 tag = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        Sharable.init(self, api)
        self.__api = api
        self.__id = id
        self.__title = title
        self.__artists = artists
        self.__headliner = headliner
        self.__venue = venue
        self.__start_date = start_date
        self.__description = description
        self.__image = image
        self.__url = url
        self.__stats = stats and Stats(
                             subject = self,
                             attendance = stats.attendance,
                             reviews = stats.reviews
                            )
        self.__tag = tag

    @property
    def id(self):
        """id of the event"""
        return self.__id

    @property
    def title(self):
        """title of the event"""
        return self.__title

    @property
    def artists(self):
        """artists performing in the event"""
        return self.__artists

    @property
    def headliner(self):
        """headliner artist of the event"""
        return self.__headliner

    @property
    def venue(self):
        """venue of the event"""
        return self.__venue

    @property
    def start_date(self):
        """start date of the event"""
        return self.__start_date

    @property
    def description(self):
        """description of the event"""
        return self.__description

    @property
    def image(self):
        """poster of the event"""
        return self.__image

    @property
    def url(self):
        """url of the event's page"""
        return self.__url

    @property
    def stats(self):
        """stats of the event"""
        return self.__stats

    @property
    def tag(self):
        """tags for the event"""
        return self.__tag
    
    def attend(self, status = STATUS_ATTENDING):
        if status not in [Event.STATUS_ATTENDING, Event.STATUS_MAYBE, Event.STATUS_NOT]:
            InvalidParametersError("status has to be 0, 1 or 2")
        params = self._default_params({'method': 'event.attend', 'status': status})
        self.__api._post_data(params)
    
    def _default_params(self, extra_params = None):
        if not self.id:
            raise InvalidParametersError("id has to be provided.")
        params = {'event': self.id}
        if extra_params is not None:
            params.update(extra_params)
        return params

    @staticmethod
    def get_info(api, event):
        params = {'method': 'event.getInfo', 'event': event}
        data = api._fetch_data(params).find('event')
        return Event.create_from_data(api, data)

    @staticmethod
    def create_from_data(api, data):
        start_date = None

        if data.findtext('startTime') is not None:
            start_date = datetime(*(
                time.strptime(
                    "%s %s" % (
                        data.findtext('startDate').strip(),
                        data.findtext('startTime').strip()
                    ),
                    '%a, %d %b %Y %H:%M'
                )[0:6])
            )
        else:
            try:
                start_date = datetime(*(
                    time.strptime(
                        data.findtext('startDate').strip(),
                        '%a, %d %b %Y %H:%M:%S'
                    )[0:6])
                )
            except ValueError:
                try:
                    start_date = datetime(*(
                        time.strptime(
                            data.findtext('startDate').strip(),
                            '%a, %d %b %Y'
                        )[0:6])
                    )
                except ValueError:
                    pass


        return Event(
                     api,
                     id = int(data.findtext('id')),
                     title = data.findtext('title'),
                     artists = [Artist(api, name = a.text) for a in data.findall('artists/artist')],
                     headliner = Artist(api, name = data.findtext('artists/headliner')),
                     venue = Venue(
                                   name = data.findtext('venue/name'),
                                   location = Location(
                                                       api,
                                                       city = data.findtext('venue/location/city'),
                                                       country = Country(
                                                            api,
                                                            name = data.findtext('venue/location/country')
                                                            ),
                                                       street = data.findtext('venue/location/street'),
                                                       postalCode = data.findtext('venue/location/postalcode'),
                                                       latitude = float(data.findtext(
                                                           'venue/location/{%s}point/{%s}lat' % ((Location.XMLNS,)*2)
                                                           )),
                                                       longitude = float(data.findtext(
                                                           'venue/location/{%s}point/{%s}long' % ((Location.XMLNS,)*2)
                                                           )),
                                                       timezone = data.findtext('venue/location/timezone')
                                                       ),
                                   url = data.findtext('venue/url')
                                   ),
                     start_date = start_date,
                     description = data.findtext('description'),
                     image = dict([(i.get('size'), i.text) for i in data.findall('image')]),
                     url = data.findtext('url'),
                     stats = Stats(
                                   subject = int(data.findtext('id')),
                                   attendance = int(data.findtext('attendance')),
                                   reviews = int(data.findtext('reviews')),
                                   ),
                     tag = data.findtext('tag')
                    )

    @staticmethod
    def hash_func(*args, **kwds):
        try:
            return hash(kwds['id'])
        except KeyError:
            raise InvalidParametersError("id has to be provided for hashing")

    def __hash__(self):
        return Event.hash_func(id = self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.start_date < other.start_date

    def __repr__(self):
        return "<lastfm.Event: %s at %s on %s>" % (self.title, self.venue.name, self.start_date.strftime("%x"))

from datetime import datetime
import time

from api import Api
from artist import Artist
from error import InvalidParametersError
from geo import Venue, Location, Country
from stats import Stats
