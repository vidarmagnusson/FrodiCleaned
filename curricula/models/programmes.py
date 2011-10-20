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
	key_competence = models.IntegerField(choices=KEY_COMPETENCE_CHOICES)
	default = models.BooleanField(default=False)
	author = models.ForeignKey(User)

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
	title = models.CharField(verbose_name=_('title of programme'), max_length=256, blank=True, default='', help_text=u'Lýsandi titill á brautinni')

	profession = models.ManyToManyField(Profession, verbose_name=_('profession'), help_text=u'Veljið námslok úr listanum hér til hliðar')

	identity = models.CharField(max_length=10, blank=True, default='', editable=False)
	unique_id = models.CharField(max_length=256, editable=False)

	description = models.TextField(blank=True, default='', verbose_name=u'Lýsing á uppbyggingu, markhópi, tengsl við atvinnulíf')

	rights_after_graduation = models.TextField(verbose_name=_('rights after graduation'), blank=True, null=True, default=None, help_text=u'Réttindi sem námslok felar í sér eða leiða til')
	
	competence_goals = models.TextField(verbose_name=_('competence goals of programme'), blank=True, default='', help_text=u'Almenn og sérhæfð hæfni nemanda að loknu námi')

	prerequisites = models.TextField(verbose_name=_('prerequisites'), blank=True, default='', help_text=u'Skilyrði sem nemandi þarf að uppfylla til að geta verið skráður á brautina')

	structure = models.TextField(verbose_name=_('organization'), blank=True, default='', help_text=u'Sérstakar áherslur sem einkenna námið')

	training = models.TextField(verbose_name=_('work training and on-site education'), blank=True, null=True, default=None, help_text=u'Skipulag, lengd og framkvæmd starfsþjálfuna og/eða vinnustaðanáms')

	progress_rules = models.TextField(verbose_name=_('rules regarding progress'), blank=True, default='', help_text=u'Skilyrði fyrir því að nemandi geti haldið áfram á braut milli ára')

	quality_assurance = models.TextField(verbose_name=_('quality assurance'), blank=True, default='', help_text=u'Aðferðir sem er beitt til að athuga hvort brautin standist allar væntingar og viðbrögð við þeim')

	key_competence_descriptions = models.ManyToManyField(KeyCompetence, verbose_name=_('foundations and key competences'), blank=True, null=True)
	key_competence_goals = models.ManyToManyField(KeyCompetenceGoal, verbose_name=_('foundation and key competence goals'), blank=True, null=True)

	evaluation = models.TextField(verbose_name=_('evaluation'), blank=True, default='', help_text=u'Almenn umfjöllun um námsmat á brautinni')

	grades = models.TextField(verbose_name=_('grades'), blank=True, default='', help_text=u'Einkunnaskali sem notaður er á brautinni.')
	previous_education = models.TextField(verbose_name=_('Evaluation of previous education'), blank=True, null=True, default='', help_text=u'Reglur um mat á fyrra námi í tengslum við brautina')
	
	credits = models.IntegerField(verbose_name=_('credits'), null=True, blank=True, default=0, help_text=u'Heildarfjöldi eininga á brautinni')

	core = models.ManyToManyField(CoursePackage, related_name='core_courses_set', blank=True, null=True, default=None, help_text=u'Skylduáfangar innan námsbrautar')
	specialization = models.ManyToManyField(CoursePackage, related_name='specializations_set', blank=True, null=True, default=None, help_text=u'Skylduáfangar sem fela í sér sérhæfingu innan brautar')
	packaged_electives = models.ManyToManyField(CoursePackage, related_name='packaged_electives_set', blank=True, null=True, default=None, help_text=u'Áfangapakkar sem nemendur geta valið um og fela í sér ákveðna áherslu')
	free_electives = models.ManyToManyField(CoursePackage, related_name='free_electives_set', blank=True, null=True, default=None, help_text=u'Áfangar sem nemendur geta valið um')

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
