from django.db import models
from django.contrib.auth.models import User
from curricula.models.fields_and_exams import Field
from curricula.models.courses import Subject
from schools.models.schools import School
from country.models.regions import Municipality
from structure.utils import slugicefy

from django.utils.translation import gettext as _

"""
Model representing a stakeholder for any curricula. Any user should be able to
add an organization as a stakeholder and mark the fields the organization is
interested in. The ministry then uses this list to find relevant stakeholder
organizations and send them notifications and call for comments.
"""
class Stakeholder(models.Model):
	name = models.CharField(_('name'), max_length=256)
	slug = models.SlugField(editable=False)
	description = models.TextField(_('description'), blank=True, null=True)
	address = models.CharField(_('address)'), max_length=128)
	municipality = models.ForeignKey(Municipality, verbose_name=_('municipality'))
	telephone = models.CharField(_('telephone'), max_length=7)
	fax = models.CharField(_('fax'), max_length=7, null=True, blank=True)
	email = models.EmailField(_('e-mail'))
	website = models.URLField(_('website'), blank=True, null=True)
	fields = models.ManyToManyField(Field, verbose_name=_('field'))
	creator = models.ForeignKey(User, editable=False)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugicefy(self.name)
		super(Stakeholder, self).save(*args, **kwargs)		

	class Meta:
		app_label = 'curricula'


"""
Information about the school which can be reused for the curricula (see
curricula app). This can only be changed by users with permissions to
change the curricula and members of the relevant school.
"""
class SchoolCurriculum(models.Model):
	# Can only be connected on one school
	school = models.OneToOneField(School, verbose_name=_('school'))

	# Curricula information fields
	activities = models.TextField(_('activities'), blank=True, null=True)
	policy = models.TextField(_('policy'), blank=True, null=True)
	administration = models.TextField(_('administration'), blank=True, null=True)
	organization = models.TextField(_('organization'), blank=True, null=True)
	instructional_methods = models.TextField(_('instructional methods'), blank=True, null=True)
	evaluation = models.TextField(_('evaluation'), blank=True, null=True)
	support_measures = models.TextField(_('support measures'), blank=True, null=True)
	student_services = models.TextField(_('student services'), blank=True, null=True)
	pupil_rights = models.TextField(_('pupil rights'), blank=True, null=True)
	cooperation = models.TextField(_('co-operation'), blank=True, null=True)
	quality_control = models.TextField(_('quality control'), blank=True, null=True)
	national_curriculum = models.TextField(_('national curriculum'), blank=True, null=True)
	other_information = models.TextField(_('other information'), blank=True, null=True)

	def __unicode__(self):
		return _('Curriculum information for %(school)s') % {'school':self.school}

	class Meta:
	        app_label = 'curricula'

		verbose_name = _('curriculum information')
		verbose_name_plural = _('curriculum information')

class CurriculumAdministrator(models.Model):
	user = models.ForeignKey(User, verbose_name=_('user'))
	school = models.ForeignKey(School, verbose_name=_('school'))
	title = models.CharField(max_length=64, verbose_name=_('title'))
	subjects = models.ManyToManyField(Subject, verbose_name=_('subjects'))

	def __unicode__(self):
		return _('%(user)s (%(title)s) in %(school)s') % {'user':self.user, 'title':self.title, 'school':self.school}

	class Meta:
		app_label = 'curricula'

		verbose_name = _('curriculum administrator')
		verbose_name_plural = _('curriculum administrators')

