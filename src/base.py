#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

class LastfmBase(object):
    """Base class for all the classes in this package"""

    @staticmethod
    def top_property(list_property_name):
        def decorator(func):
            def wrapper(ob):
                top_list = getattr(ob, list_property_name)
                return (len(top_list) and top_list[0] or None)
            return property(fget = wrapper, doc = func.__doc__)
        return decorator

    @staticmethod
    def cached_property(func):
        func_name = func.func_code.co_name
        attribute_name = "_%s" % func_name

        def wrapper(ob):
            cache_attribute = getattr(ob, attribute_name, None)
            if cache_attribute is None:
                cache_attribute = func(ob)
                setattr(ob, attribute_name, cache_attribute)
            try:
                cp = copy.copy(cache_attribute)
                return cp
            except LastfmError:
                return cache_attribute

        return property(fget = wrapper, doc = func.__doc__)

    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)

import copy
from error import LastfmError
