#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from lastfm.base import LastfmBase
from lastfm.mixins import Cacheable
from lastfm.lazylist import lazylist

class Geo(object):
    """A class representing an geographic location."""
    @staticmethod
    def get_events(api,
                  location,
                  latitude = None,
                  longitude = None,
                  distance = None):
        params = {'method': 'geo.getEvents', 'location': location}
        if distance is not None:
            params.update({'distance': distance})

        if latitude is not None and longitude is not None:
            params.update({'latitude': latitude, 'longitude': longitude})

        @lazylist
        def gen(lst):
            data = api._fetch_data(params).find('events')
            total_pages = int(data.attrib['totalpages'])

            @lazylist
            def gen2(lst, data):
                for e in data.findall('event'):
                    yield Event.create_from_data(api, e)

            for e in gen2(data):
                yield e

            for page in xrange(2, total_pages+1):
                params.update({'page': page})
                data = api._fetch_data(params).find('events')
                for e in gen2(data):
                    yield e
        return gen()

    @staticmethod
    def get_top_artists(api, country):
        params = {'method': 'geo.getTopArtists', 'country': country}
        data = api._fetch_data(params).find('topartists')
        return [
                Artist(
                       api,
                       name = a.findtext('name'),
                       mbid = a.findtext('mbid'),
                       stats = Stats(
                                     subject = a.findtext('name'),
                                     rank = int(a.attrib['rank']),
                                     playcount = int(a.findtext('playcount'))
                                     ),
                       url = 'http://' + a.findtext('url'),
                       image = {'large': a.findtext('image')}
                       )
                for a in data.findall('artist')
                ]

    @staticmethod
    def get_top_tracks(api, country, location = None):
        params = {'method': 'geo.getTopTracks', 'country': country}
        if location is not None:
            params.update({'location': location})

        data = api._fetch_data(params).find('toptracks')
        return [
                Track(
                       api,
                       name = t.findtext('name'),
                       mbid = t.findtext('mbid'),
                       artist = Artist(
                                       api,
                                       name = t.findtext('artist/name'),
                                       mbid = t.findtext('artist/mbid'),
                                       url = t.findtext('artist/url')
                                       ),
                       stats = Stats(
                                     subject = t.findtext('name'),
                                     rank = int(t.attrib['rank']),
                                     playcount = int(t.findtext('playcount'))
                                     ),
                       streamable = (t.findtext('streamable') == '1'),
                       full_track = (t.find('streamable').attrib['fulltrack'] == '1'),
                       url = 'http://' + t.findtext('url'),
                       image = {'large': t.findtext('image')}
                       )
                for t in data.findall('track')
                ]

class Location(LastfmBase, Cacheable):
    """A class representing a location of an event"""
    XMLNS = "http://www.w3.org/2003/01/geo/wgs84_pos#"

    def init(self,
                 api,
                 city = None,
                 country = None,
                 street = None,
                 postal_code = None,
                 latitude = None,
                 longitude = None,
                 timezone = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        self._api = api
        self._city = city
        self._country = country
        self._street = street
        self._postal_code = postal_code
        self._latitude = latitude
        self._longitude = longitude
        self._timezone = timezone

    @property
    def city(self):
        """city in which the location is situated"""
        return self._city

    @property
    def country(self):
        """country in which the location is situated"""
        return self._country

    @property
    def street(self):
        """street in which the location is situated"""
        return self._street

    @property
    def postal_code(self):
        """postal code of the location"""
        return self._postal_code

    @property
    def latitude(self):
        """latitude of the location"""
        return self._latitude

    @property
    def longitude(self):
        """longitude of the location"""
        return self._longitude

    @property
    def timezone(self):
        """timezone in which the location is situated"""
        return self._timezone

    @LastfmBase.cached_property
    def top_tracks(self):
        """top tracks of the location"""
        if self.country is None or self.city is None:
            raise InvalidParametersError("country and city of this location are required for calling this method")
        return Geo.get_top_tracks(self._api, self.country.name, self.city)

    @LastfmBase.top_property("top_tracks")
    def top_track(self):
        """top track of the location"""
        pass

    def get_events(self,
                  distance = None):
        return Geo.get_events(self._api,
                             self.city,
                             self.latitude,
                             self.longitude,
                             distance)

    @LastfmBase.cached_property
    def events(self):
        """events taking place at/around the location"""
        return self.get_events()

    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash("latlong%s%s" % (kwds['latitude'], kwds['longitude']))
        except KeyError:
            try:
                return hash("name%s" % kwds['city'])
            except KeyError:
                raise InvalidParametersError("either latitude and longitude or city has to be provided for hashing")

    def __hash__(self):
        if not self.city:
            return self.__class__._hash_func(
                                           latitude = self.latitude,
                                           longitude = self.longitude)
        else:
            return self.__class__._hash_func(name = self.city)

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude

    def __lt__(self, other):
        if self.country != other.country:
            return self.country < other.country
        else:
            return self.city < other.city

    def __repr__(self):
        if self.city is None:
            return "<lastfm.geo.Location: (%s, %s)>" % (self.latitude, self.longitude)
        else:
            return "<lastfm.geo.Location: %s>" % self.city

class Country(LastfmBase, Cacheable):
    """A class representing a country."""
    ISO_CODES = {
         'AD': 'Andorra',
         'AE': 'United Arab Emirates',
         'AF': 'Afghanistan',
         'AG': 'Antigua and Barbuda',
         'AI': 'Anguilla',
         'AL': 'Albania',
         'AM': 'Armenia',
         'AN': 'Netherlands Antilles',
         'AO': 'Angola',
         'AQ': 'Antarctica',
         'AR': 'Argentina',
         'AS': 'American Samoa',
         'AT': 'Austria',
         'AU': 'Australia',
         'AW': 'Aruba',
         'AX': 'land Islands',
         'AZ': 'Azerbaijan',
         'BA': 'Bosnia and Herzegovina',
         'BB': 'Barbados',
         'BD': 'Bangladesh',
         'BE': 'Belgium',
         'BF': 'Burkina Faso',
         'BG': 'Bulgaria',
         'BH': 'Bahrain',
         'BI': 'Burundi',
         'BJ': 'Benin',
         'BL': 'Saint Barthlemy',
         'BM': 'Bermuda',
         'BN': 'Brunei Darussalam',
         'BO': 'Bolivia',
         'BR': 'Brazil',
         'BS': 'Bahamas',
         'BT': 'Bhutan',
         'BV': 'Bouvet Island',
         'BW': 'Botswana',
         'BY': 'Belarus',
         'BZ': 'Belize',
         'CA': 'Canada',
         'CC': 'Cocos (Keeling) Islands',
         'CD': 'Congo, The Democratic Republic of the',
         'CF': 'Central African Republic',
         'CG': 'Congo',
         'CH': 'Switzerland',
         'CI': "Cte d'Ivoire",
         'CK': 'Cook Islands',
         'CL': 'Chile',
         'CM': 'Cameroon',
         'CN': 'China',
         'CO': 'Colombia',
         'CR': 'Costa Rica',
         'CU': 'Cuba',
         'CV': 'Cape Verde',
         'CX': 'Christmas Island',
         'CY': 'Cyprus',
         'CZ': 'Czech Republic',
         'DE': 'Germany',
         'DJ': 'Djibouti',
         'DK': 'Denmark',
         'DM': 'Dominica',
         'DO': 'Dominican Republic',
         'DZ': 'Algeria',
         'EC': 'Ecuador',
         'EE': 'Estonia',
         'EG': 'Egypt',
         'EH': 'Western Sahara',
         'ER': 'Eritrea',
         'ES': 'Spain',
         'ET': 'Ethiopia',
         'FI': 'Finland',
         'FJ': 'Fiji',
         'FK': 'Falkland Islands (Malvinas)',
         'FM': 'Micronesia, Federated States of',
         'FO': 'Faroe Islands',
         'FR': 'France',
         'GA': 'Gabon',
         'GB': 'United Kingdom',
         'GD': 'Grenada',
         'GE': 'Georgia',
         'GF': 'French Guiana',
         'GG': 'Guernsey',
         'GH': 'Ghana',
         'GI': 'Gibraltar',
         'GL': 'Greenland',
         'GM': 'Gambia',
         'GN': 'Guinea',
         'GP': 'Guadeloupe',
         'GQ': 'Equatorial Guinea',
         'GR': 'Greece',
         'GS': 'South Georgia and the South Sandwich Islands',
         'GT': 'Guatemala',
         'GU': 'Guam',
         'GW': 'Guinea-Bissau',
         'GY': 'Guyana',
         'HK': 'Hong Kong',
         'HM': 'Heard Island and McDonald Islands',
         'HN': 'Honduras',
         'HR': 'Croatia',
         'HT': 'Haiti',
         'HU': 'Hungary',
         'ID': 'Indonesia',
         'IE': 'Ireland',
         'IL': 'Israel',
         'IM': 'Isle of Man',
         'IN': 'India',
         'IO': 'British Indian Ocean Territory',
         'IQ': 'Iraq',
         'IR': 'Iran, Islamic Republic of',
         'IS': 'Iceland',
         'IT': 'Italy',
         'JE': 'Jersey',
         'JM': 'Jamaica',
         'JO': 'Jordan',
         'JP': 'Japan',
         'KE': 'Kenya',
         'KG': 'Kyrgyzstan',
         'KH': 'Cambodia',
         'KI': 'Kiribati',
         'KM': 'Comoros',
         'KN': 'Saint Kitts and Nevis',
         'KP': "Korea, Democratic People's Republic of",
         'KR': 'Korea, Republic of',
         'KW': 'Kuwait',
         'KY': 'Cayman Islands',
         'KZ': 'Kazakhstan',
         'LA': "Lao People's Democratic Republic",
         'LB': 'Lebanon',
         'LC': 'Saint Lucia',
         'LI': 'Liechtenstein',
         'LK': 'Sri Lanka',
         'LR': 'Liberia',
         'LS': 'Lesotho',
         'LT': 'Lithuania',
         'LU': 'Luxembourg',
         'LV': 'Latvia',
         'LY': 'Libyan Arab Jamahiriya',
         'MA': 'Morocco',
         'MC': 'Monaco',
         'MD': 'Moldova',
         'ME': 'Montenegro',
         'MF': 'Saint Martin',
         'MG': 'Madagascar',
         'MH': 'Marshall Islands',
         'MK': 'Macedonia, The Former Yugoslav Republic of',
         'ML': 'Mali',
         'MM': 'Myanmar',
         'MN': 'Mongolia',
         'MO': 'Macao',
         'MP': 'Northern Mariana Islands',
         'MQ': 'Martinique',
         'MR': 'Mauritania',
         'MS': 'Montserrat',
         'MT': 'Malta',
         'MU': 'Mauritius',
         'MV': 'Maldives',
         'MW': 'Malawi',
         'MX': 'Mexico',
         'MY': 'Malaysia',
         'MZ': 'Mozambique',
         'NA': 'Namibia',
         'NC': 'New Caledonia',
         'NE': 'Niger',
         'NF': 'Norfolk Island',
         'NG': 'Nigeria',
         'NI': 'Nicaragua',
         'NL': 'Netherlands',
         'NO': 'Norway',
         'NP': 'Nepal',
         'NR': 'Nauru',
         'NU': 'Niue',
         'NZ': 'New Zealand',
         'OM': 'Oman',
         'PA': 'Panama',
         'PE': 'Peru',
         'PF': 'French Polynesia',
         'PG': 'Papua New Guinea',
         'PH': 'Philippines',
         'PK': 'Pakistan',
         'PL': 'Poland',
         'PM': 'Saint Pierre and Miquelon',
         'PN': 'Pitcairn',
         'PR': 'Puerto Rico',
         'PS': 'Palestinian Territory, Occupied',
         'PT': 'Portugal',
         'PW': 'Palau',
         'PY': 'Paraguay',
         'QA': 'Qatar',
         'RE': 'Runion',
         'RO': 'Romania',
         'RS': 'Serbia',
         'RU': 'Russian Federation',
         'RW': 'Rwanda',
         'SA': 'Saudi Arabia',
         'SB': 'Solomon Islands',
         'SC': 'Seychelles',
         'SD': 'Sudan',
         'SE': 'Sweden',
         'SG': 'Singapore',
         'SH': 'Saint Helena',
         'SI': 'Slovenia',
         'SJ': 'Svalbard and Jan Mayen',
         'SK': 'Slovakia',
         'SL': 'Sierra Leone',
         'SM': 'San Marino',
         'SN': 'Senegal',
         'SO': 'Somalia',
         'SR': 'Suriname',
         'ST': 'Sao Tome and Principe',
         'SV': 'El Salvador',
         'SY': 'Syrian Arab Republic',
         'SZ': 'Swaziland',
         'TC': 'Turks and Caicos Islands',
         'TD': 'Chad',
         'TF': 'French Southern Territories',
         'TG': 'Togo',
         'TH': 'Thailand',
         'TJ': 'Tajikistan',
         'TK': 'Tokelau',
         'TL': 'Timor-Leste',
         'TM': 'Turkmenistan',
         'TN': 'Tunisia',
         'TO': 'Tonga',
         'TR': 'Turkey',
         'TT': 'Trinidad and Tobago',
         'TV': 'Tuvalu',
         'TW': 'Taiwan, Province of China',
         'TZ': 'Tanzania, United Republic of',
         'UA': 'Ukraine',
         'UG': 'Uganda',
         'UM': 'United States Minor Outlying Islands',
         'US': 'United States',
         'UY': 'Uruguay',
         'UZ': 'Uzbekistan',
         'VA': 'Holy See (Vatican City State)',
         'VC': 'Saint Vincent and the Grenadines',
         'VE': 'Venezuela',
         'VG': 'Virgin Islands, British',
         'VI': 'Virgin Islands, U.S.',
         'VN': 'Viet Nam',
         'VU': 'Vanuatu',
         'WF': 'Wallis and Futuna',
         'WS': 'Samoa',
         'YE': 'Yemen',
         'YT': 'Mayotte',
         'ZA': 'South Africa',
         'ZM': 'Zambia',
         'ZW': 'Zimbabwe'}
    def init(self,
                 api,
                 name = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        self._api = api
        self._name = name

    @property
    def name(self):
        """name of the country"""
        return self._name

    @LastfmBase.cached_property
    def top_artists(self):
        """top artists of the country"""
        return Geo.get_top_artists(self._api, self.name)

    @LastfmBase.top_property("top_artists")
    def top_artist(self):
        """top artist of the country"""
        pass

    def get_top_tracks(self, location = None):
        return Geo.get_top_tracks(self._api, self.name, location)

    @LastfmBase.cached_property
    def top_tracks(self):
        """top tracks of the country"""
        return self.get_top_tracks()

    @LastfmBase.top_property("top_tracks")
    def top_track(self):
        """top track of the country"""
        pass

    @LastfmBase.cached_property
    def events(self):
        """events taking place at/around the location"""
        return Geo.get_events(self._api, self.name)

    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash(kwds['name'].lower())
        except KeyError:
            raise InvalidParametersError("name has to be provided for hashing")

    def __hash__(self):
        return self.__class__._hash_func(name = self.name)

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.geo.Country: %s>" % self.name

from lastfm.api import Api
from lastfm.artist import Artist
from lastfm.error import InvalidParametersError
from lastfm.event import Event
from lastfm.stats import Stats
from lastfm.track import Track
