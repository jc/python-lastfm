#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

import types

class Xml2Dict (dict):

	def __init__(self, parent):
		self.update(dict([('@' + item[0], item[1]) for item in parent.items()]))
		
		for child in parent:
		#	print child.tag
			if child:
				if not child.tag in self:
					self[child.tag] = Xml2Dict(child)
				else:
					if type(self[child.tag]) != types.ListType:
						self[child.tag] = [self[child.tag]]
					self[child.tag].append(Xml2Dict(child))

			if not child and child.items():
				if not child.tag in self:
					self[child.tag] = dict([('@' + item[0], item[1]) for item in child.items()])
				else:
					if type(self[child.tag]) != types.ListType:
						self[child.tag] = [self[child.tag]]
					self[child.tag].append(
						dict([('@' + item[0], item[1]) for item in child.items()])
					)


			if child.text:
				if not child.tag in self:
					self[child.tag] = child.text.strip() or None
				elif child.text.strip():
					if type(self[child.tag]) != types.ListType:
						flag = False
						for e in self[child.tag].keys():
							if e.startswith('@'):
								flag = True
						if not flag:
							self[child.tag] = [self[child.tag]]
							self[child.tag][0].update({'text': child.text.strip()})
						else:
							self[child.tag].update({'text': child.text.strip()})
					else:
						self[child.tag][-1].update({'text': child.text.strip()})
			if not child.tag in self:
				self[child.tag] = None
