from django.db import models

from django.utils.translation import gettext as _

"""
Model describing a Creative Commons license which can then be used to license
content and contribute it to the common pool of free culture. Makes it easier
to manage copyright. All content on the site should be released under one of
the CC licenses since the site is built around sharing. It was either this
approach or the "this site owns everything you upload"-approach. This is way
nicer.
"""
class License(models.Model):
	# Title, e.g. Creative Commons Attribution Share Alike 3.0
	title = models.CharField(_('title of license'), max_length=96)

	# URL of CC website (with more detail about the license)
	url = models.URLField(_('creativecommons.org url'))

	# URL to representative images (large and small) used to mark the work
	image_mark_large = models.URLField(_('large representative image'))
	image_mark_small = models.URLField(_('small representative image'))

	# Abbreviation of license, e.g. cc-by-sa
	text_mark = models.CharField(_('license abbreviation'), max_length=11)

	def __unicode__(self):
		return self.title

	def html_mark(self, author):
		return '<a rel="license" href="%(license_url)s"><img src="%(image_url)s" alt="%(text_mark)s"></a> <div xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">%(author)s</div>' % {'license_url':self.url, 'image_url':self.image_mark_large, 'text_mark':self.text_mark, 'author':author}

	def html_mark_small(self, author):
		return '<a rel="license" href="%(license_url)s"><img src="%(image_url)s" alt="%(text_mark)s"></a> <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">%(author)s</span>' % {'license_url':self.url, 'image_url':self.image_mark_small, 'text_mark':self.text_mark, 'author':author}
