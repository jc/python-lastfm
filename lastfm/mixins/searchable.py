#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from lastfm.lazylist import lazylist

class Searchable(object):
    @classmethod
    def search(cls,
               api,
               search_item,
               limit = None,
               **kwds):
        from lastfm.api import Api
        cls_name = cls.__name__.lower()
        params = {
                  'method': '%s.search'%cls_name,
                  cls_name: search_item
                  }
        for kwd in kwds:
            if kwds[kwd] is not None:
                params[kwd] = kwds[kwd]

        if limit:
            params.update({'limit': limit})

        @lazylist
        def gen(lst):
            data = api._fetch_data(params).find('results')
            total_pages = int(data.findtext("{%s}totalResults" % Api.SEARCH_XMLNS))/ \
                            int(data.findtext("{%s}itemsPerPage" % Api.SEARCH_XMLNS)) + 1

            @lazylist
            def gen2(lst, data):
                for a in data.findall('%smatches/%s'%(cls_name, cls_name)):
                    yield cls._search_yield_func(api, a)

            for a in gen2(data):
                yield a

            for page in xrange(2, total_pages+1):
                params.update({'page': page})
                data = api._fetch_data(params).find('results')
                for a in gen2(data):
                    yield a
        return gen()

    @staticmethod
    def _search_yield_func(api, search_term):
        pass
