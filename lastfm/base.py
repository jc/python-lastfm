#!/usr/bin/env python
"""Module containting the base class for all the classes in this package"""

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm"

from lastfm.lazylist import lazylist

class LastfmBase(object):
    """Base class for all the classes in this package"""
    
    @classmethod
    def get_all(cls, seed, hash_attrs, spider_func):
        if cls == LastfmBase:
            raise NotImplementedError("the subclass must implement this method")
        @lazylist
        def gen(lst):
            seen = []
            api = seed._api
            
            def hash_dict(item):
                return dict((a, getattr(item, a)) for a in hash_attrs)
            
            seen.append(hash_dict(seed))
            yield seed
            for hsh in seen:
                for n in spider_func(api, hsh):
                    if hash_dict(n) not in seen:
                        seen.append(hash_dict(n))
                        yield n
        return gen()
    
    def __eq__(self, other):
        raise NotImplementedError("The subclass must override this method")
    
    def __lt__(self, other):
        raise NotImplementedError("The subclass must override this method")

    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq__(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)