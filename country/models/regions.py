from django.db import models
from structure.utils import slugicefy

from django.utils.translation import gettext as _

"""
A country can be split into multiple regions or country areas
This model represent country areas with names, descriptions and
coordinate points based on svg (used to draw the country onto a
html5 canvas in different colors depending on the surroundings
"""
class CountryArea(models.Model):
	name = models.CharField(_('name'), max_length=128)
	slug = models.SlugField(editable=False)
	description = models.TextField(_('description'), blank=True, null=True)
	# Coordinate points must be entered in relation to one another or the
	# map cannot be drawn correctly
	points = models.TextField(_('coordinate points'), blank=True, null=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugicefy(self.name)
		super(CountryArea, self).save(*args, **kwargs)

	class Meta:
		ordering = ['name']
		app_label = 'country'
 
		verbose_name = _('country area')
		verbose_name_plural = _('country areas')


"""
Municipalities in a country are represented in this model. Each municipality
has a unique postal code or zip code, a name, possibly some logo and then a
link to a region in the country (we can then plot the region the municipality
is in on a map
"""
class Municipality(models.Model):
	postal_code = models.PositiveIntegerField(_('zip code'), unique=True)
	name = models.CharField(_('name'), max_length=128)
	logo = models.URLField(_('logo'), blank=True, null=True)
	area = models.ForeignKey(CountryArea, verbose_name=_('area'))

	def __unicode__(self):
		return '%d %s' % (self.postal_code, self.name)

	class Meta:
		ordering = ['postal_code']
		app_label = 'country'

		verbose_name = _('municipality')
		verbose_name_plural = _('municipalities')
