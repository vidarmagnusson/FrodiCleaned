from django.db import models
from django.contrib.auth.models import User
from Frodi.schools.models.schools import School

from django.utils.translation import gettext as _

"""
Model representing a student society within a school. It is most likely that
this model will only be linked to secondary schools or universities. About
each of these societies we want to know the name, the school and a description.
Besides that all other information is optional (such as logo, board members,
website). School staff with permissions can create new societies and board
members of it can change the information
"""
class StudentSociety(models.Model):
    name = models.CharField(_('name'), max_length=256)
    school = models.ForeignKey(School, verbose_name=_('school'))
    description = models.TextField(_('description'))
    website = models.URLField(_('website'), blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    board_members = models.ManyToManyField(User, through='StudentSocietyMembers', verbose_name=_('board members'), blank=True, null=True)
    logo = models.URLField(_('logo'), blank=True, null=True)
    photo = models.URLField(_('representative photo'), blank=True, null=True)
    video = models.URLField(_('introductory video'), blank=True, null=True)

    def __unicode__(self):
        return self.school, '-', self.name

    class Meta:
        app_label = 'schools'
        ordering = ['school', 'name']

        verbose_name = _('student society')
        verbose_name_plural = _('student societies')

class StudentSocietyMembers(models.Model):
    title = models.CharField(max_length=256)
    member = models.ForeignKey(User)
    student_society = models.ForeignKey(StudentSociety)

    class Meta:
        app_label = 'schools'
        
