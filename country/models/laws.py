from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from django.utils.translation import gettext as _

from roman import toRoman
from markdown import markdown

"""
A model to represent a law on a specific topic. The structure of the laws
follows that of laws in Iceland where the is a law, e.g. Copyright law, which
has sections in it and each section has a number of articles in it. Each
article then has paragraphs but they are represented with normal html paragraphs
(or markdown paragraphs for input). So this model descripes a law.
"""
class Law(models.Model):
	# Title, number and description of the law
	title = models.CharField(_('title'), max_length=256)
	number = models.CharField(_('number'), max_length=128, blank=True, null=True)
	description = models.TextField(_('description'), blank=True, null=True)

	# A URL that points to the official version of the law (this allows the
	# laws on this site to deviate, e.g. hyperlinks (and better link names
	# like "see [SECTION NAME]" instead of numbers nobody understands
	url = models.URLField(_('URL of original version'))

	# We might want to be able to distinguish laws based on the site to be
	# able to collect all laws around, e.g. education, using a manager
	sites = models.ManyToManyField(Site)
	objects = models.Manager()
        on_site = CurrentSiteManager(field_name='sites')

	def __unicode__(self):
		return u'%s - %s' % (self.title, self.number)

	class Meta:
	        app_label = 'country'

		verbose_name = _('law')
		verbose_name_plural = _('laws')


"""
A model representing a section within a specific law. This follows the Icelandic
structure of laws. Each section can have a number, title and maybe a desription
"""
class Section(models.Model):
	number = models.PositiveIntegerField(_('number'))
	title = models.CharField(_('title'), max_length=256)
	description = models.TextField(_('description'), blank=True, null=True)

	# We connect this section to a specific law instance
	law = models.ForeignKey(Law, verbose_name=_('law'))

	def __unicode__(self):
		# The Icelandic tradition of marking sections within laws is to
		# use roman numericals. The string representation of the law is
		# therefore a roman numerical with title (and we add the law in
		# parantheses to show what law it belongs to
		return _('Chapter %(number)s - %(title)s (%(law)s)') % {'number':toRoman(self.number), 'title':self.title, 'law':self.law}

	class Meta:
		ordering = ['number']
	        app_label = 'country'

		verbose_name = _('law section')
		verbose_name_plural = _('law sections')


"""
A model representing an article within a section of a specific law. This follows
the Icelandic structure of laws. Each article can have a number, a subnumber 
(i.e. a, b, c, etc.) and a title but must have content. For speed we store a 
html version of the content as well and use markdown to convert the content to 
the html version of the content
"""
class Article(models.Model):
	# Number, subnumber and title can be included
	number = models.PositiveIntegerField(_('number'), blank=True, null=True)
	subnumber = models.CharField(_('subnumber'), max_length=3, blank=True, null=True)
	title = models.CharField(_('title'), max_length=512, blank=True, null=True)

	# Content must be included. We use markdown as input format of articles
	# and then convert it to a html representation
	content = models.TextField(_('content'))
	html_content = models.TextField(editable=False)

	# Connect to article to a specific law section
	section = models.ForeignKey(Section, verbose_name=_('law section'))

	def save(self, *args, **kwargs):
		# Use markdown to create a html version of the content
		self.html_content = markdown(self.content)
		super(Article, self).save(*args, **kwargs)

	def __unicode__(self):
		# We default the returned name to an empty string
		name = ''

		# If the article has a number we add a number to the name
		if self.number:
			name = _('Article %(number)d') % {'number':self.number}

		# If the article has a subnumber append it to the name
		if self.subnumber and self.subnumber != '':
			name = '%s %s' % (name, self.subnumber)
		
		# If the article has a title append it to the name
		if self.title and self.title != '':
			name = '%s %s' % (name, self.title)

		# If the article does not have a number nor a title we return
		# the first few (lets say 20) characters of the content
		if name == '':
			self.name = self.content[:20]

		return name
	
	class Meta:
		ordering = ['number']
	        app_label = 'country'

		verbose_name = _('law article')
		verbose_name_plural = _('law articles')
