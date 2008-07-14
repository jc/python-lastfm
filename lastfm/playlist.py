#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Playlist(LastfmBase, str):
    """A class representing an XPSF playlist."""
    def init(self, xpsfData, playlistUrl):
        self = xpsfData
        self.__playlistUrl = playlistUrl

    def getPlaylistUrl(self):
        return self.__playlistUrl

    playlistUrl = property(getPlaylistUrl, None, None, "PlaylistUrl's Docstring")
        
    @staticmethod
    def fetch(api, playlistUrl):
        params = {'method': 'playlist.fetch'}
        return Playlist(api.fetchData(params, parse = False), playlistUrl)
    
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['playlistUrl'])
        except KeyError:
            raise LastfmError("playlistUrl has to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(playlistUrl = self.playlistUrl)
    
    def __eq__(self, other):
        return self.playlistUrl == other.playlistUrl
    
    def __lt__(self, other):
        return self.playlistUrl < other.playlistUrl
    
    def __repr__(self):
        return "<lastfm.Playlist: %s>" % self.playlistUrl