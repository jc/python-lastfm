#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
from lazylist import lazylist

class Searchable(object):
    @classmethod
    def search(cls,
               api,
               searchItem,
               limit = None,
               **kwds):
        from api import Api
        clsName = cls.__name__.lower()
        params = {
                  'method': '%s.search'%clsName,
                  clsName: searchItem
                  }
        for kwd in kwds:
            if kwds[kwd] is not None:
                params[kwd] = kwds[kwd]

        if limit:
            params.update({'limit': limit})
            
        @lazylist
        def gen(lst):
            data = api._fetchData(params).find('results')
            totalPages = int(data.findtext("{%s}totalResults" % Api.SEARCH_XMLNS))/ \
                            int(data.findtext("{%s}itemsPerPage" % Api.SEARCH_XMLNS)) + 1
            
            @lazylist
            def gen2(lst, data):
                for a in data.findall('%smatches/%s'%(clsName, clsName)):
                    yield cls._searchYieldFunc(api, a)
                          
            for a in gen2(data):
                yield a
            
            for page in xrange(2, totalPages+1):
                params.update({'page': page})
                data = api._fetchData(params).find('results')
                for a in gen2(data):
                    yield a
        return gen()