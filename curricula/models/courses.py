#! -*- encoding: utf-8 -*-

# Curriculum - Web application for creating and managing educational curricula
# Copyright (C) 2010  The Ministry of Education, Science and Culture, Iceland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

import uuid

class Subject(models.Model):
	name = models.CharField(max_length=128)
	author = models.ForeignKey(User, editable=False)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.lower()
		super(Subject, self).save(*args,**kwargs)
    
	class Meta:
		app_label = 'curricula'
		verbose_name = _('subject')
		verbose_name_plural = _('subjects')

class SubjectCombination(models.Model):
	combination = models.ManyToManyField(Subject)
	abbreviation = models.CharField(max_length=4)
	author = models.ForeignKey(User, editable=False)
	
	def __unicode__(self):
		return "%s - %s" % (self.abbreviation, self.subjects())

	# Returns an array of subjects belonging to this combination
	def subjects_list(self):
		return [x.name for x in self.combination.all()]

	# Returns a comma separated string of all subjects in this combination
	def subjects(self):
		return ", ".join(self.subjects_list())

	def save(self, *args, **kwargs):
		self.abbreviation = self.abbreviation.upper()
		super(SubjectCombination, self).save(*args, **kwargs)
        
	class Meta:
		app_label = 'curricula'
		ordering = ['abbreviation']
		verbose_name = _('subject combination')
		verbose_name_plural = _('subjects combinations')

class Topic(models.Model):
	name = models.CharField(max_length=128)
	author = models.ForeignKey(User, editable=False)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.lower()
		super(Topic, self).save(*args, **kwargs)

	class Meta:
		app_label = 'curricula'
		verbose_name = _('topic')
		verbose_name_plural = _('topics')

class TopicCombination(models.Model):
	combination = models.ManyToManyField(Topic)
	subject = models.ForeignKey(SubjectCombination)
	abbreviation = models.CharField(max_length=2)
	author = models.ForeignKey(User, editable=False)

	def __unicode__(self):
		return "%s - %s" % (self.abbreviation, self.topics())

	def save(self, *args, **kwargs):
		self.abbreviation = self.abbreviation.upper()
		super(TopicCombination, self).save(*args, **kwargs)

	# Returns an array of topics belonging to this combination
	def topics_list(self):
		return [x.name for x in self.combination.all()]

	# Returns a comma separated string of all topics in this combination
	def topics(self):
		return ", ".join(self.topics_list())
    
	class Meta:
		app_label = 'curricula'
		verbose_name = _('topic combination')
		verbose_name_plural = _('topics combinations')

def subjectcombination_find_by_set(subjects):
	if subjects == None:
		return None

	possible = SubjectCombination.objects.filter(combination__in=subjects)
	for p in possible:
		if set(p.combination.all()) == set(subjects):
			return p
	return None

def topiccombination_find_by_set(topics, subjectcombination):
	if subjectcombination == None or topics == None:
		return None

	possible = TopicCombination.objects.filter(combination__in=topics)
	for p in possible:
		if set(p.combination.all()) == set(topics) and p.subject == subjectcombination:
			return p
	return None

def topiccombination_find_all(topics):
	possible = TopicCombination.objects.filter(combination__in=topics)
	return [p for p in possible if set(p.combination.all()) == set(topics)]

def topiccombination_find_any(topics):
	suggestions = set([])
	for topic in topics:
		suggestions = suggestions | set([(tc.abbreviation, tc.topics()) for tc in topic.topiccombination_set.all()])

	return [{'abbreviation':a,'topics':t} for (a,t) in suggestions]

def subject_abbreviation_free(abbreviation):
	a = SubjectCombination.objects.filter(abbreviation=abbreviation.upper())
	if len(a) > 0:
		return False
	return True

def topic_abbreviation_free(abbreviation, subjectcombination):
	a = TopicCombination.objects.filter(subject=subjectcombination)
	a = a.filter(abbreviation=abbreviation.upper())
	if len(a) > 0:
		return False
	return True

class Goal(models.Model):
	goal = models.CharField(max_length=256)
	author = models.ManyToManyField(User, editable=False)

	def __unicode__(self):
		return self.goal

	class Meta:
		app_label = 'curricula'

class Evaluation(models.Model):
	goal = models.ForeignKey(Goal)
	evaluation = models.TextField()
	author = models.ManyToManyField(User, editable=False)

	def __unicode__(self):
		return self.evaluation

	class Meta:
		app_label = 'curricula'
		verbose_name = _('evaluation')
		verbose_name_plural = _('evaluations')


class Course(models.Model):
	STATUS_CHOICES = ( 
			(1, _('In progress')),
			(2, _('Ready for inspection')),
			(3, _('Approved by school')),
			(4, _('Officially approved')), 
			(5, _('Rejected by school')),
			(6, _('Rejected officially')),
			)

	LEVEL_CHOICES = (
			(1, _('Level 1')),
			(2, _('Level 2')),
			(3, _('Level 3')),
			(4, _('Level 4')),
		 	)

	descriptive_name = models.CharField(verbose_name=_('descriptive name'), max_length=255, default='', blank=True, help_text='Stutt setning sem lýsir innihaldi námskeiðsins')
# _('Write a short sentence which describes the subject and the topic of the course. Examples of descriptive names are: 21st century Icelandic art history, Maintenance control of machines, Sales and services, German pronunciation and vocabulary, Hair coloring, Linux administration.')

	subjects = models.ForeignKey(SubjectCombination, blank=True, verbose_name=_('subjects'), help_text='Grunnsvið eða fög sem eru kennd (aðgreind með kommu)')
# _('Write or choose from the list to the right a subject that describes the foundational area of expertise which is taught in the course. Examples of subjects are: Mathematics, Icelandic, chemistry, electrical circuits, first aid, media, hair styling, industrial control, machine handling, management, electrical engineering, industrial architecture. It is permissible to name more than one subjects (separated by a comma) when creating multi-disciplinary courses.')

	topics = models.ForeignKey(TopicCombination, blank=True, verbose_name=_('topics'), help_text='Helstu umfjöllunarefni (aðgreind með kommu)')
# _('Write or choose from the list to the right one to four of the most influential topics of the course. Separate the topics by a comma. Examples of topics are: Pedagogy, genetics, statistics, grammar, alternating currents, machine architecture, welding. Keep in mind that only two letters will represent the topic in the course abbreviation')

	level = models.IntegerField(_('level'), choices=LEVEL_CHOICES, default=1, help_text='Hæfniþrep sem að minnsta kosti 75% af námskeiðinu er á ')
# _("Make a suggestion about the course's competence level. Choose the corresponding competence level below. Note that at least 75%% of the course topics should belong to the course's competence level")

	credits = models.IntegerField(_('school credits'), default=0, blank=True, help_text='Hver eining samsvarar þriggja daga vinnu nemenda (6-8 klst/dag)')
# _('Here is the scope of the course given in school credits. A school credit is the measurement of an average student work contribution in school, disregarding whether the studies are practical or theoretical and whether it takes place within or outside the school. Each school credit translates to about three days of work (6-8 hours a day) for the student. It is advised to keep the competence goals in mind when estimating work contribution and assigning school credits. (To use old school credits it is necessary to configure the schools information accordingly. This system will automatically translate between the two credits systems according to the formula: school credits = old credits x 60/35.)')

	description = models.TextField(_('description'), default='', blank=True, help_text=_('A short description of the main content of the course'))

	prerequisites = models.TextField(_('prerequisites'), default='', blank=True, help_text='Lýsing á skilyrðum sem nemendur þurfa að uppfylla til að mega taka námskeiðið')
# _('Here are listed the prerequisites for the course if there are any. Prerequisites can for example be specific courses that the student must have passed before or at the same time as this course, the amount of school credits for a specific topic on a specific level or any other description of prerequisites the student must fulfill.')

	knowledge_goals = models.ManyToManyField(Goal, verbose_name=_('knowledge goals'), related_name='knowledge_goals', blank=True, null=True, help_text='2-10 atriði sem lýsa staðreyndum, lögmálum og aðferðum sem nemendur eiga að þekkja og skilja')
# _('Knowledge goals describe the knowledge the student shall have acquired by passing the course. Knowledge ranges from facts to laws to processes and is both theoretical and applicable. The course evaluation takes these goals into account. On average 2 to 10 goals are expected to be added as continuation of the following sentence: A studet shall have acquired knowledge and understanding of:')

	skills_goals = models.ManyToManyField(Goal, verbose_name=_('skill goals'), related_name='skills_goals', blank=True, null=True, help_text='2-10 atriði sem lýsa aðferðum og verklagi sem nemendur eiga að geta beitt')
# _('Skill goals describe the skills the student shall have acquired by passing the course. Skills can be both mental and practical and allow the student to apply methods and processes. The course evaluation takes these goals into account. On average 2 to 10 goals are expected to be added as continuation of the following sentence: A student shall have acquired the skills to: Verbs related to skills are e.g. apply, inspect, use, speak, write, draw, calculate, express, do, construct, manage...')

	competence_goals = models.ManyToManyField(Goal, verbose_name=_('competence goals'), related_name='competence_goals', blank=True, null=True, help_text='2-10 atriði sem lýsa getu nemenda til að samþætta þekkingu og leikni með mælanlegum hætti')
# _('Competence goals describe the competence the student shall have acquired by passing the course. Competence means the overlook and ability to apply the knowledge and skills. These goals must therefore relate to or build upon the knowlede and skill goals of the course. Care must be taken to allow the competence goals to be evaluated. After writing each comptence goals one can describe its evaluation to make it easier to write the competence goals with evaluation in mind. Examples of evaluation methods can be: Oral exams, peer evaluation, guided evaluation, self-evaluation, evaluation of oral debates, normal debates, talks, presentations, arguments, work processes, work organization, finishing, resourcefulness, communications, responsible/consciencous work contribution ... On average 2 to 10 goals are expected to be added as continuation of the following sentence: A student shall be able to apply the general knowledge and skills he/she has acquired to: Verbs and phrases that relate to competence are e.g. gather, use, express, debate, explain, describe, participate, relate ... to, be active, be responsible, be able to, argue, understand, show initiative, do, work, evaluate ...')

	evaluation = models.TextField(_('evaluation'), blank=True, null=True, help_text='Almenn umfjöllun um námsmat og námsmatsaðferðir áfangans')
# _('Here is a general description of evaluation and evaluation methods used in the course to evaluate the knowledge, skills and competences which the student has acquired in the course and worked according to the goals set forward in the course description. This is not the place to put ratios between evaluation techniques, that information belongs to the course syllabus')

	status = models.IntegerField(_('status'), default=1, choices=STATUS_CHOICES, editable=False)
	modification_date = models.DateTimeField(_('last modified'), default=datetime.now, editable=False)

	history = models.ForeignKey('Course', blank=True, null=True, verbose_name=_('derived from'))
	author = models.ForeignKey(User, related_name='author', blank=True, verbose_name=_('author'), help_text='Upphaflegi höfundur áfangans')
	coauthors = models.ManyToManyField(User, related_name='coauthors', blank=True, verbose_name=_('co-authors'), help_text='Notendur sem mega breyta áfanganum')
# _("The curricula system allows many individuals to collaborate on courses. It is easy to give others a chance to review, comment on, and improve the course, even if they work within or outside of your school. You as an author can choose co-authors. Author and co-authors are assigned while the course is being designed and created. When a course has been approved by school officals and added to a curricula database and connected to a programme, authors will not be attributed. Here below is a list of possible co-authors. The list contains persons you follow in the community who have access to the curricula database. If somebody is missing from the list you need to subscribe to that person in the community and/or ask the curricula managers in that person's school to give them access to the curricula database.")

	name = models.CharField(_('course abbreviation'), max_length=9, blank=True, editable=False)
	version = models.IntegerField(_('version number'), blank=True, null=True, editable=False)

	unique_id = models.CharField(max_length=256, editable=False)

	def __unicode__(self):
		return self.id_name()

	def authors_for_url(self):
		return '-'.join([a.username for a in self.author.all()])

	def id_name(self):
		if self.version:
			return u'%s_%s' % (self.name, self.version)
		return self.name

	def increase_status(self):
		max_status = len(STATUS_CHOICE)
		if self.status < max_status:
			self.status = self.status+1

		if self.status == max_status:
			max_agg = Course.objects.filter(name=self.name).aggregate(Max(version))
			if max_agg['version__max']:
				self.version = max_agg['version__max']+1
			else:
				self.version = 0

		self.save()

	def save(self, *args, **kwargs):
		if not self.unique_id:
			self.unique_id = str(uuid.uuid1())

		self.name = u'%s%s%s%s' % (self.subjects.abbreviation, self.level, self.topics.abbreviation, '%02d' % self.credits)
		super(Course, self).save()

	class Meta:
		app_label = 'curricula'
		verbose_name = _('course')
		verbose_name_plural = _('courses')

class ExemplaryCourse(models.Model):
	course = models.ForeignKey(Course, verbose_name=_('exemplary course'))
	
	name_subjects_and_topics = models.TextField(verbose_name=_('subjects, topics and the descriptive name'), blank=True, null=True)

	description = models.TextField(verbose_name=_('description'), blank=True, null=True)
	prerequisites = models.TextField(verbose_name=_('prerequisites'), blank=True, null=True)
	level = models.TextField(verbose_name=_('course level'), blank=True, null=True)

	goals = models.TextField(verbose_name=_('competence goals'), blank=True, null=True)

	competence_evaluation = models.TextField(verbose_name=_('evaluation of competence_goals'), blank=True, null=True)

	competence_goals_and_credits = models.TextField(verbose_name=_('competence goals and credits'), blank=True, null=True)

	evaluation = models.TextField(verbose_name=_('course evaluation'), blank=True, null=True)

	def __unicode__(self):
		return _('Exemplary course: %(course)s') % {'course':self.course.name}

	def exemplary_list(self):
		exemplary_list = []
		for field in self._meta.fields:
			if field.name not in ['id','course']:
				value = getattr(self, field.name)
				if value:
					exemplary_list.append(field.verbose_name)

		return exemplary_list

	class Meta:
		app_label = 'curricula'
		verbose_name = _('exemplary course')
		verbose_name_plural = _('exemplary courses')

