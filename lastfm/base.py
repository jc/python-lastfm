#!/usr/bin/env python
"""Module containting the base class for all the classes in this package"""

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

class LastfmBase(object):
    """Base class for all the classes in this package"""

    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)