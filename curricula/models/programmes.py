# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from curricula.models.courses import Course, SubjectCombination
from curricula.models.fields_and_exams import Profession, ExamLevel, Exam
from django.utils.translation import ugettext as _

import uuid

class SubjectLevel(models.Model):
	subject = models.ForeignKey(SubjectCombination)
	level = models.PositiveIntegerField(choices=Course.LEVEL_CHOICES)

	class Meta:
		app_label = 'curricula'
		verbose_name = _('subject level')
		verbose_name_plural = _('subject levels')

class ExtraRule(models.Model):
	title = models.CharField(verbose_name=_('title'), max_length=256)
	exam = models.ForeignKey(Exam, verbose_name=_('exam'))
	subject = models.ManyToManyField(SubjectLevel, verbose_name=_('subject'))
	minimum_credits = models.PositiveIntegerField(verbose_name=_('minimum credits'))

	def __unicode__(self):
		return self.title

	class Meta:
		app_label = 'curricula'
		verbose_name = _('extra rule')
		verbose_name_plural = _('extra rules')

class KeyCompetence(models.Model):
	KEY_COMPETENCE_CHOICES = ( 
		(1, _('Education Competence')),
		(2, _('Health')),
		(3, _('Creative thinking and knowledge application')),
		(4, _('Equality')),
 		(5, _('Democracy and human rights')),
		(6, _('Education for sustainability')),
		(7, _('Reading, expression, communication in the mother language')),
		(8, _('Reading, expression, communication in foreign languages')),
		(9, _('Reading, expression, communication of numbers and information')),
		)

	description = models.TextField()
	key_competence = models.IntegerField(choices=KEY_COMPETENCE_CHOICES, editable=False)
	default = models.BooleanField(default=False, editable=False)
	author = models.ForeignKey(User, editable=False)

	def __unicode__(self):
		return '%s (%s)' % (self.description[:64], self.get_key_competence_display())

	class Meta:
		app_label = 'curricula'
		verbose_name = _('key competence')
		verbose_name_plural = _('key competences')

class KeyCompetenceGoal(models.Model):
	goal = models.CharField(max_length=256)
	key_competence = models.IntegerField(choices=KeyCompetence.KEY_COMPETENCE_CHOICES, editable=False)
	author = models.ForeignKey(User, editable=False)

	class Meta:
		app_label = 'curricula'
		verbose_name = _('key competence goal')
		verbose_name_plural = _('key competence goals')

class CoursePackage(models.Model):
	title = models.CharField(verbose_name=_('title'), max_length=128)
	author = models.ForeignKey(User, verbose_name=_('author'))
	courses = models.ManyToManyField(Course, verbose_name=_('courses'))

	def __unicode__(self):
		return self.title

	class Meta:
		app_label = 'curricula'
		verbose_name = _('course package')
		verbose_name_plural = _('course packages')

class Programme(models.Model):
	title = models.CharField(verbose_name=_('title of programme'), max_length=256, blank=True, default='', help_text=_('A descriptive title for the programme'))
	profession = models.ManyToManyField(Profession, verbose_name=_('profession'), help_text=_('The resulting professions of the programme'))

	identity = models.CharField(max_length=10, blank=True, default='', editable=False)
	unique_id = models.CharField(max_length=256, editable=False)

	description = models.TextField(blank=True, default='', verbose_name=_('general description'))

	rights_after_graduation = models.TextField(verbose_name=_('rights after graduation'), blank=True, null=True, default=None)
	
	competence_goals = models.TextField(verbose_name=_('competence goals of programme'), blank=True, default='')


	prerequisites = models.TextField(verbose_name=_('prerequisites'), blank=True, default='')
	structure = models.TextField(verbose_name=_('organization'), help_text=_('organization of programme'), blank=True, default='')
	training = models.TextField(verbose_name=_('work training and on-site education'), blank=True, null=True, default=None)
	progress_rules = models.TextField(verbose_name=_('rules regarding progress'), help_text=_('rules that must be fulfilled for student to progress in his or her studies'), blank=True, default='')
	quality_assurance = models.TextField(verbose_name=_('quality assurance'), blank=True, default='')

	key_competence_descriptions = models.ManyToManyField(KeyCompetence, verbose_name=_('foundations and key competences'), blank=True, null=True)
	key_competence_goals = models.ManyToManyField(KeyCompetenceGoal, verbose_name=_('foundation and key competence goals'), blank=True, null=True)

	evaluation = models.TextField(verbose_name=_('evaluation'), blank=True, default='')
	grades = models.TextField(verbose_name=_('grades'), blank=True, default='')
	previous_education = models.TextField(verbose_name=_('Evaluation of previous education'), blank=True, null=True, default='')
	
	credits = models.IntegerField(verbose_name=_('credits'), null=True, blank=True, default=0, help_text=_('The total amount of credits for this programme.'))

	core = models.ManyToManyField(CoursePackage, related_name='core_courses_set', blank=True, null=True, default=None)
	specialization = models.ManyToManyField(CoursePackage, related_name='specializations_set', blank=True, null=True, default=None)
	packaged_electives = models.ManyToManyField(CoursePackage, related_name='packaged_electives_set', blank=True, null=True, default=None)
	free_electives = models.ManyToManyField(CoursePackage, related_name='free_electives_set', blank=True, null=True, default=None)

	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, related_name='programme_author')
	coauthors = models.ManyToManyField(User, related_name='programme_coauthors')


	def save(self, *args, **kwargs):
		if not self.unique_id:
			self.unique_id = str(uuid.uuid1())

		super(Programme, self).save()

	class Meta:
		app_label = 'curricula'
		verbose_name = _('programme')
		verbose_name_plural = _('programmes')
