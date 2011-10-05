from django.db import models
from django.contrib.auth.models import User
from FrodiWork.schools.models.schools import SecondarySchool
from curricula.models.programmes import Programme

from django.utils.translation import gettext as _

"""
Information regarding registration into schools. At the moment only connected
to secondary schools since that is under the supervision of the ministry but
can easily be modified to include registration information for other school
levels. This model will very likely take some changes in future versions
"""
class RegistrationInformation(models.Model):
    school = models.ForeignKey(SecondarySchool, verbose_name=_('school'))
    contact_person = models.ManyToManyField(User, verbose_name=_('contact person'))
    contact_email = models.EmailField(_('email address of contact person'))
    contact_telephone = models.CharField(_('telephone number of contact person'), max_length=7, blank=True, null=True)
    programmes = models.ManyToManyField(Programme, verbose_name=_('programmes'))
    
    registration_start = models.DateField(_('start date of registration'))
    registration_end = models.DateField(_('end date of registration'))

    # For automatic computations of probable schools prerequisites should then
    # be stated in a more machine readable way (in the future)
    prerequisites = models.TextField(_('acceptance prerequisites'), blank=True, null=True)

    def __unicode__(self):
        return _('Registration information for %(programmes)s in %(school)s') % {'programmes':', '.join(self.programmes.all()), 'school':self.school}

    class Meta:
        app_label = 'schools'

        verbose_name = _('registration information')
        verbose_name_plural = _('registration information')
