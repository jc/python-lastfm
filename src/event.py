#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Event(LastfmBase):
    """A class representing an event."""
    def init(self,
                 api,
                 id = None,
                 title = None,
                 artists = None,
                 headliner = None,
                 venue = None,
                 startDate = None,
                 startTime = None,
                 description = None,
                 image = None,
                 url = None,
                 stats = None,
                 tag = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__id = id
        self.__title = title
        self.__artists = artists
        self.__headliner = headliner
        self.__venue = venue
        self.__startDate = startDate
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
    def startDate(self):
        """start date of the event"""
        return self.__startDate

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

    @staticmethod
    def getInfo(api, event):
        params = {'method': 'event.getinfo', 'event': event}
        data = api._fetchData(params).find('event')
        return Event.createFromData(api, data)

    @staticmethod
    def createFromData(api, data):
        startDate = None

        if data.findtext('startTime') is not None:
            startDate = datetime(*(
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
                startDate = datetime(*(
                    time.strptime(
                        data.findtext('startDate').strip(),
                        '%a, %d %b %Y %H:%M:%S'
                    )[0:6])
                )
            except ValueError:
                try:
                    startDate = datetime(*(
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
                                                           'venue/location/{%s}point/{%s}lat' % ((Location.xmlns,)*2)
                                                           )),
                                                       longitude = float(data.findtext(
                                                           'venue/location/{%s}point/{%s}long' % ((Location.xmlns,)*2)
                                                           )),
                                                       timezone = data.findtext('venue/location/timezone')
                                                       ),
                                   url = data.findtext('venue/url')
                                   ),
                     startDate = startDate,
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
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['id'])
        except KeyError:
            raise LastfmError("id has to be provided for hashing")

    def __hash__(self):
        return Event.hashFunc(id = self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.startDate < other.startDate

    def __repr__(self):
        return "<lastfm.Event: %s at %s on %s>" % (self.title, self.venue.name, self.startDate.strftime("%x"))

from datetime import datetime
import time

from api import Api
from artist import Artist
from error import LastfmError
from geo import Venue, Location, Country
from stats import Stats
