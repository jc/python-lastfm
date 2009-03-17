#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm.mixins"

from lastfm.mixins.cacheable import Cacheable
from lastfm.mixins.searchable import Searchable
from lastfm.mixins.sharable import Sharable
from lastfm.mixins.shoutable import Shoutable
from lastfm.mixins.taggable import Taggable

__all__ = ['Cacheable', 'Searchable', 'Sharable', 'Shoutable', 'Taggable']