from django.db import models
from django.contrib.auth.models import User
from country.models.regions import Municipality
from FrodiWork.schools.models.housing import Housing
from feedzilla.models import Feed
from structure.utils import slugicefy

from django.utils.translation import gettext as _

"""
Static (or mostly static) information regarding schools.
Can only be updated by ministry officials. Classes indicating
the types of the school inherit this one
"""
class School(models.Model):
	# Name and identification number of the school
	name = models.CharField(_('name'), max_length=256)
	slug = models.SlugField(editable=False)
	identity_number = models.CharField(_('identity number'), max_length=10)

	# Address and municipalities
	address = models.CharField(_('address'), max_length=128)
	# Link to municipality in country app - based on zip code
	municipality = models.ForeignKey(Municipality, 
					 verbose_name=_('municipality'))

	telephone = models.CharField(_('telephone'), max_length=7, blank=True, null=True)

	# Schools may or may not have a fax number
	fax = models.CharField(_('fax'), max_length=7, null=True, blank=True)

	# Email is necessary but a website may or may not exist
	email = models.EmailField(_('e-mail'), blank=True, null=True)
	website = models.URLField(_('website'), null=True, blank=True)

	# The school's benevolent ruler may or may not be a user of the site
	principal = models.ForeignKey(User, verbose_name=_('principal'), blank=True, null=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugicefy(self.name)
		super(School, self).save(*args, **kwargs)

	class Meta:
		ordering = ['name']
	        app_label = 'schools'

		verbose_name = _('school')
		verbose_name_plural = _('schools')


"""
Model representing the preschools (which are schools).
Preschool might have an official name which stems from 
the reason that preschools can be run by municipalities 
and registered as such.
"""
class Preschool(School):
	official_name = models.CharField(_('official name'), max_length=256, 
					 blank=True, null=True)

	class Meta:
	        app_label = 'schools'

		verbose_name = _('preschool')
		verbose_name_plural = _('preschools')

"""
Model representing the primary schools (which are schools).
Primary schools might have an official name which stems from 
the reason that primary schools can be run by municipalities 
and registered as such.
"""
class PrimarySchool(School):
	official_name = models.CharField(_('official name'), max_length=256, 
					 blank=True, null=True)

	class Meta:
	        app_label = 'schools'

		verbose_name = _('primary school')
		verbose_name_plural = _('primary schools')

"""
Model representing secondary schools (which are schools).
Secondary schools have an abbreviation which they are usually known
by. This might not be the case everywhere though
"""
class SecondarySchool(School):
	abbreviation = models.CharField(_('abbreviation'), max_length=16, 
					blank=True, null=True)

	def save(self, *args, **kwargs):
		# When saving we ensure the abbreviation is lowercased
		if self.abbreviation:
			self.abbreviation = self.abbreviation.lower()
		super(SecondarySchool, self).save(*args, **kwargs)

	class Meta:
	        app_label = 'schools'

		verbose_name = _('secondary school')
		verbose_name_plural = _('secondary schools')


"""
Model representing universities (which are schools).
Universities have an abbreviation which they are usually known
by. This might not be the case everywhere though
"""
class University(School):
	abbreviation = models.CharField(_('abbreviation'), max_length=16, 
					blank=True, null=True)

	def save(self, *args, **kwargs):
		# When saving we ensure the abbreviation is lowercased
		if self.abbreviation:
			self.abbreviation = self.abbreviation.lower()
		super(University, self).save(*args, **kwargs)

	class Meta:
	        app_label = 'schools'

		verbose_name = _('university')
		verbose_name_plural = _('universities')

"""
Model representing learning centers (which can be regarded as schools)
Learning centers may or may not have an abbreviation. This might not
be the case everywhere. This model might have to be modified in later
versions of the software
"""
class LearningCenter(School):
	abbreviation = models.CharField(_('abbreviation'), max_length=16, 
					blank=True, null=True)

	def save(self, *args, **kwargs):
		# When saving we ensure the abbreviation is lowercased
		if self.abbreviation:
			self.abbreviation = self.abbreviation.lower()
		super(LearningCenter, self).save(*args, **kwargs)

	class Meta:
	        app_label = 'schools'

		verbose_name = _('learning center')
		verbose_name_plural = _('learning centers')

"""
Information about the school such as a description, logos, rss feeds, etc.
This information is maintained by the schools themselves, by designated
teachers or other members of the staff.
"""
class SchoolInformation(models.Model):
	# School information is only connected to one school
	school = models.OneToOneField(School, verbose_name=_('school'))

	# Description of the school is not necessary (although recommended)
	description = models.TextField(_('description'), blank=True, null=True)

	# A school can have a student housing option, we link to it here since
	# two or more schools might offer the same student housing
	student_housing = models.ForeignKey(Housing, verbose_name=_('student housing'), blank=True, null=True)

	# Graphics for schools to make it prettier on the site
	# Graphics include a logo, a representative photo and a video
	logo = models.URLField(_('logo'), blank=True, null=True)
	photo = models.URLField(_('representative photo'), blank=True, null=True)
	video = models.URLField(_('introductory video'), blank=True, null=True)

	# Members of the school, can be staff, teachers, students or other
	# stakeholders (such as parents or others who want to follow the school)
	members = models.ManyToManyField(User, verbose_name=_('members'), editable=False, through='SchoolMember')

	# RSS or Atom feed for the school to display news on this site. Uses
	# a feedzilla feed
	feed = models.OneToOneField(Feed, verbose_name=_('feed'), blank=True, null=True)

	def __unicode__(self):
		return _(u'School Information for %(school)s') % {'school':self.school}

	class Meta:
	        app_label = 'schools'

		verbose_name = _('school information')
		verbose_name_plural = _('school information')

"""
Through table used to connect users and school information giving each user
a choice of member type (staff, teacher, pupil, stakeholder).
"""
class SchoolMember(models.Model):
	MEMBER_CHOICES = ((0, _('Staff')),
			  (1, _('Teacher')),
			  (2, _('Pupil')),
			  (3, _('Stakeholder')),)

	school_information = models.ForeignKey(SchoolInformation)
	member = models.ForeignKey(User)
	member_type = models.IntegerField(choices=MEMBER_CHOICES)

	class Meta:
	        app_label = 'schools'
