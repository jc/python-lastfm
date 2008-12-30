#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from safelist import SafeList

class Taggable(object):
    def init(self, api):
        self.__api = api
        
    @LastfmBase.cachedProperty
    def tags(self):
        from tag import Tag
        params = self._default_params({'method': '%s.getTags' % self.__class__.__name__.lower()})
        data = self.__api._fetch_data(params, sign = True, session = True, no_cache = True).find('tags')
        return SafeList([
                       Tag(
                           self.__api,
                           name = t.findtext('name'),
                           url = t.findtext('url')
                           )
                       for t in data.findall('tag')
                       ],
                       self.add_tags, self.remove_tag)
    
    def add_tags(self, tags):
        from tag import Tag
        while(len(tags) > 10):
                        section = tags[0:9]
                        tags = tags[9:]
                        self.add_tags(section)
        
        if len(tags) == 0: return

        tagnames = []
        for tag in tags:
            if isinstance(tag, Tag):
                tagnames.append(tag.name)
            elif isinstance(tag, str):
                tagnames.append(tag)
        
        params = self._default_params({
            'method': '%s.addTags' % self.__class__.__name__.lower(),
            'tags': ",".join(tagnames)
            })       
        self.__api._post_data(params)
        self.__tags = None
        
    def remove_tag(self, tag):
        from tag import Tag
        if isinstance(tag, Tag):
            tag = tag.name
            
        params = self._default_params({
            'method': '%s.removeTag' % self.__class__.__name__.lower(),
            'tag': tag
            })
        self.__api._post_data(params)
        self.__tags = None
        
    def _default_params(self, extra_params):
        pass