from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.contrib.sites.managers import CurrentSiteManager
from structure.utils import slugicefy
from creativecommons.models import License

from django.utils.translation import ugettext as _

class Menu(models.Model):
	title = models.CharField(max_length=128, verbose_name=_('title'))
	icon = models.ImageField(upload_to='menu_icons', verbose_name=_('icon'), blank=True, null=True)
	slug = models.SlugField(verbose_name=_('slug'), editable=False)
	url = models.CharField(max_length=255, verbose_name=_('url'), blank=True)
	parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, related_name='children')
	order = models.IntegerField(verbose_name=_('order'), blank=True, null=True)
	sites = models.ManyToManyField(Site, verbose_name=_('sites'))
	groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, null=True)
	objects = models.Manager()
	on_site = CurrentSiteManager(field_name='sites')
	
	def __unicode__(self):
		return ' - '*(self.url.count('/')-1) + self.title

	def save(self, *args, **kwargs):
		self.slug = slugicefy(self.title)

		flatpage = None
		try:
			flatpage = FlatPage.on_site.get(url=self.url)
		except:
			pass
		
		if self.parent:
			self.url = '/'.join([self.parent.url[:-1], self.slug, ''])
		else:
			self.url = '/'

		if flatpage:
			flatpage.url = self.url
			flatpage.save()

		super(Menu, self).save(*args, **kwargs)

		for child in self.children.all():
			child.save()

	class Meta:
		unique_together = (('url', 'title'),)
		ordering = ('url', 'order', 'title')

		verbose_name = _('menu')
		verbose_name_plural = _('menus')

class Slide(models.Model):
	title = models.CharField(max_length=16, verbose_name=_('title'))
	order = models.IntegerField(verbose_name=_('order'))

	summary = models.CharField(max_length=64, verbose_name=_('summary'))
	description = models.TextField(verbose_name=_('description'))

	see_more_text = models.CharField(max_length=32, verbose_name=_('text description for more information'), blank=True, null=True)
	see_more_link = models.URLField(verbose_name=_('link to more information'), blank=True, null=True)
	
	image = models.URLField(verbose_name=_('representative image'))
	license = models.ForeignKey(License, verbose_name=_('license'), blank=True, null=True)
	author = models.CharField(max_length=256, verbose_name=_('original author'), blank=True, null=True)
	author_link = models.URLField(verbose_name=_('url of original author'), blank=True, null=True)
	
	def __unicode__(self):
		return self.title

	def author_with_url(self):
		return '<a href="%(author_url)s" title="%(author)s">%(author)s</a>' % {'author_url':self.author_link, 'author':self.author}

	class Meta:
		ordering = ('order', 'title')

		verbose_name= _('slide')
		verbose_name_plural = _('slides')

class Highlight(models.Model):
        title = models.CharField(max_length=128, verbose_name=_('title'))
        link = models.CharField(max_length=128, verbose_name=_('link'))
	icon = models.ImageField(upload_to='highlight_icons', verbose_name=_('icon'), blank=True, null=True)
        order = models.IntegerField(verbose_name=_('order'))
        pages = models.ManyToManyField('Menu', verbose_name=_('pages'), blank=False, related_name='highlights')

	def __unicode__(self):
                return self.title

        class Meta:
                ordering = ('title', 'order')

		verbose_name = _('highlight')
		verbose_name_plural = _('highlights')
