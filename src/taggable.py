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
        
        params = self._defaultParams({'method': '%s.getTags' % self.__class__.__name__.lower()})
        data = self.__api._fetchData(params, sign = True, session = True, no_cache = True).find('tags')
        return SafeList([
                       Tag(
                           self.__api,
                           name = t.findtext('name'),
                           url = t.findtext('url')
                           )
                       for t in data.findall('tag')
                       ],
                       self.addTags, self.removeTag)
    
    def addTags(self, tags):
        from tag import Tag
        while(len(tags) > 10):
                        section = tags[0:9]
                        tags = tags[9:]
                        self.addTags(section)
        
        if len(tags) == 0: return

        tagnames = []
        for tag in tags:
            if isinstance(tag, Tag):
                tagnames.append(tag.name)
            elif isinstance(tag, str):
                tagnames.append(tag)
        
        params = self._defaultParams({
            'method': '%s.addTags' % self.__class__.__name__.lower(),
            'tags': ",".join(tagnames)
            })       
        self.__api._postData(params)
        self.__tags = None
        
    def removeTag(self, tag):
        from tag import Tag
        if isinstance(tag, Tag):
            tag = tag.name
            
        params = self._defaultParams({
            'method': '%s.removeTag' % self.__class__.__name__.lower(),
            'tag': tag
            })
        self.__api._postData(params)
        self.__tags = None