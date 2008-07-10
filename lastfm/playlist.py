#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Playlist(str):
    """A class representing an XPSF playlist."""
    def __init__(self, xpsfData):
        self = xpsfData
        
    @staticmethod
    def fetch(api, playlistUrl):
        params = {'method': 'playlist.fetch'}
        return Playlist(api.fetchData(params, parse = False))