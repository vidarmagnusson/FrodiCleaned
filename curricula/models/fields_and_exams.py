from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Field(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=256)
    standard_id = models.CharField(verbose_name=_('id according to standard'), max_length=1)
    description = models.TextField(verbose_name=_('description'))
    
    def __unicode__(self):
        return u'%s %s' % (self.standard_id, self.title)
    
    class Meta:
        app_label = 'curricula'
        ordering = ['standard_id']
        verbose_name = _('field')
        verbose_name_plural = _('fields')
        
class SubField(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=256)
    standard_id = models.CharField(verbose_name=_('id according to standard'), max_length=1)
    description = models.TextField(verbose_name=_('description'))
    field = models.ForeignKey(Field, verbose_name=_('subfield of'))
    
    def __unicode__(self):
        return u'%s%s %s' % (self.field.standard_id, self.standard_id, self.title)

    class Meta:
        app_label = 'curricula'
        ordering = ['field__standard_id', 'standard_id']
        verbose_name = _('subfield')
        verbose_name_plural = _('subfields')
        
class ExamLevel(models.Model):
    LEVEL_CHOICES = (
        (1, _('Level 1')),
        (2, _('Level 2')),
        (3, _('Level 3')),
        (4, _('Level 4')),
        )
    
    level = models.PositiveIntegerField(verbose_name=_('level'), choices=LEVEL_CHOICES)	
    
    min_ratio_level_one = models.PositiveIntegerField(verbose_name=('minimum ratio on level one'))
    max_ratio_level_one = models.PositiveIntegerField(verbose_name=('maximum ratio on level one'))
    
    min_ratio_level_two = models.PositiveIntegerField(verbose_name=('minimum ratio on level two'), blank=True, null=True)
    max_ratio_level_two = models.PositiveIntegerField(verbose_name=('maximum ratio on level two'), blank=True, null=True)
    
    min_ratio_level_three = models.PositiveIntegerField(verbose_name=('minimum ratio on level three'), blank=True, null=True)
    max_ratio_level_three = models.PositiveIntegerField(verbose_name=('maximum ratio on level three'), blank=True, null=True)
    
    min_ratio_level_four = models.PositiveIntegerField(verbose_name=('minimum ratio on level four'), blank=True, null=True)
    max_ratio_level_four = models.PositiveIntegerField(verbose_name=('maximum ratio on level four'), blank=True, null=True)
    
    def __unicode__(self):
        return _(u'Level %d') % (self.level)	
    
    class Meta:
        app_label = 'curricula'
        verbose_name = _('exam level')
        verbose_name_plural = _('exam levels')

        
class Exam(models.Model):
    title = models.CharField(verbose_name=_('exam title'), unique=True, max_length=128)
    description = models.TextField(verbose_name=_('description'))
    level = models.ForeignKey(ExamLevel)
    
    minimum_credits = models.PositiveIntegerField(verbose_name=_('minimum credits'))
    maximum_credits = models.PositiveIntegerField(verbose_name=_('maximum credits'))

    def __unicode__(self):
        return self.title
    
    class Meta:
        app_label = 'curricula'
        verbose_name = _('exam')
        verbose_name_plural = _('exams')

class Profession(models.Model):
    STATUS_CHOICES = ( 
        (1, _('Unapproved')),
        (2, _('Officially approved')), 
        )

    title = models.CharField(verbose_name=_('title'), max_length=256)
    description = models.TextField(verbose_name=_('description'))

    exam = models.ForeignKey(Exam, verbose_name=_('exam level'))
    status = models.IntegerField(_('status'), default=1, choices=STATUS_CHOICES, editable=False)

    creator = models.ForeignKey(User, verbose_name=_('author'))
    field = models.ForeignKey(SubField, verbose_name=_('field'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
	self.title = self.title.lower()
	super(Profession, self).save(*args, **kwargs)
    
    class Meta:
        app_label = 'curricula'
        verbose_name = _('profession')
        verbose_name_plural = _('professions')
