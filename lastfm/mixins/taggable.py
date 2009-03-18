#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm.mixins"

from lastfm.safelist import SafeList
from lastfm.decorators import cached_property, authenticate

class Taggable(object):
    def init(self, api):
        self._api = api
        
    @cached_property
    @authenticate
    def tags(self):
        from lastfm.tag import Tag
        params = self._default_params({'method': '%s.getTags' % self.__class__.__name__.lower()})
        data = self._api._fetch_data(params, sign = True, session = True, no_cache = True).find('tags')
        return SafeList([
                       Tag(
                           self._api,
                           name = t.findtext('name'),
                           url = t.findtext('url')
                           )
                       for t in data.findall('tag')
                       ],
                       self.add_tags, self.remove_tag)
    
    @authenticate
    def add_tags(self, tags):
        from lastfm.tag import Tag
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
        self._api._post_data(params)
        self._tags = None
        
    @authenticate
    def remove_tag(self, tag):
        from lastfm.tag import Tag
        if isinstance(tag, Tag):
            tag = tag.name
            
        params = self._default_params({
            'method': '%s.removeTag' % self.__class__.__name__.lower(),
            'tag': tag
            })
        self._api._post_data(params)
        self._tags = None
        
    def _default_params(self, extra_params = None):
        if extra_params is not None:
            return extra_params
        else:
            return {}