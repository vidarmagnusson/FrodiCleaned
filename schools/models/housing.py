from django.db import models
from django.contrib.auth.models import User
from country.models.regions import Municipality
#from community.models import PhotoAlbum

from django.utils.translation import gettext as _

"""
Student housing model. Managers within each school can create a student
housing and link it to the school. They can then set the manager of the
student housing which can change the information about it (as long as the
manager is a user) along with the school.
"""
class Housing(models.Model):
	title = models.CharField(_('title'), max_length=128)
	description = models.TextField(_('description'))
	address = models.CharField(_('address'), max_length=128)
	municipality = models.ForeignKey(Municipality, verbose_name=_('municipality'))
	email = models.EmailField(_('e-mail'))
	extra_information = models.URLField(_('URL for more information'), blank=True, null=True)
	manager = models.ForeignKey(User, verbose_name=_('manager'), blank=True, null=True)
	telephone = models.CharField(_('telephone'), max_length=7, blank=True, null=True)
	fax = models.CharField(_('fax'), max_length=7, blank=True, null=True)
#	album = models.OneToOneField('PhotoAlbum', verbose_name=_('housing album'), blank=True, null=True)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'schools'

		verbose_name = _('student housing')
		verbose_name_plural = _('student housings')


"""
Model containing information about a specific room in a student housing
and the amount of these rooms available. Each of these can then have a room
album which can contain photos, floor plans, etc.
"""
class RoomType(models.Model):
	title = models.CharField(_('title'), max_length=256)
	description = models.TextField(_('description'))
	monthly_rent = models.PositiveIntegerField(_('monthly rent'))
	housing = models.ForeignKey(Housing, verbose_name=_('student housing'))

	amount = models.IntegerField(_('available amount'), blank=True, null=True)
	size = models.DecimalField(_('size in square meters'), max_digits=3, decimal_places=1, blank=True, null=True)
#	room_album = models.OneToOneField('PhotoAlbum', verbose_name=_('room album'), blank=True, null=True)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'schools'

		verbose_name = _('room type')
		verbose_name_plural = _('room types')


"""
Services offered at the student housing. These services include
laundry service, cafeteria, food courts, public telephones, internet
access, etc. Each service can offer different services under different
prices (e.g. breakfast, lunch, dinner) so this model includes only the 
title, description and the connection to a student housing.
"""
class Service(models.Model):
	title = models.CharField(_('title'), max_length=256)
	description = models.TextField(_('description'))
	housing = models.ForeignKey(Housing, verbose_name=_('student housing'))

	class Meta:
		app_label = 'schools'

		verbose_name = _('housing service')
		verbose_name_plural = _('housing services')

"""
A service offering for a specific service. This is a specific item being
offered as a part of a service. Internet connection might for example be
the service and each service offering would then be the different bandwidth
the pupils are offered (at different prices). Includes description since it
might be necessary to include a description such as if laundry is only
available on Mondays and Thursdays or whatever is necessary to explain.
"""
class ServiceOffering(models.Model):
	title = models.CharField(_('title'), max_length=256)
	description = models.TextField(_('description'), blank=True, null=True)
	price = models.PositiveIntegerField(_('price'))
	service = models.ForeignKey(Service, verbose_name=_('service'))

	class Meta:
		app_label = 'schools'

		verbose_name = _('service offering')
		verbose_name_plural = _('service offerings')
