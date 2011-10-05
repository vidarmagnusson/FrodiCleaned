#! -*- encoding: utf-8 -*-
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.forms.widgets import RadioSelect, HiddenInput
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard import FormWizard
from django.contrib.admin import widgets
from django.http import HttpResponseRedirect
from markdown import markdown
from structure.utils import cloudify

from django.utils.translation import ugettext as _

from curricula.models.courses import Course, SubjectCombination, TopicCombination, Goal, Evaluation, Subject, Topic, ExemplaryCourse
from curricula.forms.widgets import SliderInput, AddGoalInput, RenderLevels, MultipleAuthorInput
from community.models import Person


"""
Used when the form is submitted"
"""
class CourseForm(ModelForm):
	class Meta:
		model = Course

"""
Used to create an exemplary course
"""
class ExemplaryCourseForm(ModelForm):
    class Meta:
        model = ExemplaryCourse

"""
Step one in the form creation
"""
class CourseCreateForm(ModelForm):
	class Meta:
		model = Course
		fields = ('subjects', 'topics')

"""
Step two in the form creation
"""
class CourseDescriptionForm(ModelForm):
	class Meta:
		model = Course
		fields = ('descriptive_name', 'level', 'description', 'prerequisites')
		widgets = {'level':RadioSelect(renderer=RenderLevels)}

"""
Step three in the form creation
"""
class CourseGoalForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(CourseGoalForm, self).__init__(*args, **kwargs)
		self.fields['knowledge_goals'].help_text = self.fields['knowledge_goals'].help_text.replace(_('Hold down "Control", or "Command" on a Mac, to select more than one.'), '')
		self.fields['skills_goals'].help_text = self.fields['skills_goals'].help_text.replace(_('Hold down "Control", or "Command" on a Mac, to select more than one.'), '')
		self.fields['competence_goals'].help_text = self.fields['competence_goals'].help_text.replace(_('Hold down "Control", or "Command" on a Mac, to select more than one.'), '')

	class Meta:
		model = Course
		fields = ('knowledge_goals', 'skills_goals', 'competence_goals', 'credits')
		widgets = {'knowledge_goals':AddGoalInput(), 'skills_goals':AddGoalInput(), 'competence_goals':AddGoalInput(),
			   'credits':SliderInput(attrs={'unit':'fein.', 'min':1, 'max':15})}

"""
Step four in the form creation
Optional evaluation text field and the ability to choose co-authors for
the course
"""

class CourseEvaluationAuthorForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(CourseEvaluationAuthorForm, self).__init__(*args, **kwargs)

		# Get the user profile
		user = kwargs['initial']['user']
		# All permissions uses must have to be possible authors
		permissions = ['curricula.add_course', 'curricula.delete_course',
				'curricula.add_subject', 'curricula.delete_subject',
				'curricula.add_topic', 'curricula.delete_topic',
				'curricula.add_subjectcombination', 'curricula.delete_subjectcombination',
				'curricula.add_topiccombination', 'curricula.delete_topiccombination',
				'curricula.add_goal', 'curricula.delete_goal',
				'curricula.add_evaluation', 'curricula.delete_evaluation']

		self.fields['coauthors'].help_text = self.fields['coauthors'].help_text.replace(_('Hold down "Control", or "Command" on a Mac, to select more than one.'), '')
		self.fields['coauthors'].choices = [f for f in user.find_following() if f.user.has_perms(permissions)]

	class Meta:
		model = Course
		fields = ('evaluation','coauthors')
		widgets = {'coauthors':MultipleAuthorInput()}

"""
Main course wizard
"""
class CourseWizard(FormWizard):
	def done(self, request, form_list):
            try:
                course = Course.objects.get(unique_id=self.extra_context['unique_id'])
            except:
                        print "Course was not found"
                        return HttpResponseRedirect('/')
            
            for form in form_list:
                for field, value in form.cleaned_data.iteritems():
                    setattr(course, field, value)
                    
            course.author = request.user
            course.save()
            return HttpResponseRedirect(reverse('view-course', kwargs={'id':course.unique_id}))

	def process_step(self, request, form, step):
            # Save the course in between steps
            # Since process_step is run for every step up to the
            # submitted step we must compare it to the submitted step
            # (called wizard_step)
            if step == int(request.POST.get('wizard_step',0)):
                # If the submitted step is the first step
                # We create a new course object and set its id
                # in the extra context (so that it follows all the way through)
                if step == 0:
                    try:
                        course = Course.objects.create(subjects=SubjectCombination.objects.get(id=form['subjects'].data), topics=TopicCombination.objects.get(id=form['topics'].data), author=request.user)
                        course.save()
                    except:
                        print "Unable to create a course"
                        return self.render_revalidation_failure(request, step, form)

                    self.extra_context['unique_id'] = course.unique_id
                # If we are passed the first step we fetch the course based
                # on the id in the extra context and update the course
                else:
                    try:
			course = Course.objects.get(unique_id=self.extra_context['unique_id'])
                    except:
                        print "Course was not found"
                        return self.render_revalidation_failure(request, step, form)

                    for field, value in form.cleaned_data.iteritems():
                        setattr(course, field, value)
                    course.save()

            if step == 1:
                maximum_credits = 15
                minimum_credits = 1
                
                self.initial[2] = {'credits':minimum_credits,
                                   'maximum_credits':maximum_credits,
                                   'minimum_credits':minimum_credits}
                
            if step == 2:
                print 'User', request.user
                print 'Person', request.user.get_profile()
                self.initial[3] = {'user':request.user.get_profile()}

	def render_template(self, request, form, previous_fields, step, context=None):
		if not context:
			context = {}

		ctx = context
                    
		previous_values = []

		"""
		Variables for storing strings while the user hasn't entered any data.
		"""
		name_subjects = '----'
		name_level = '-'
		name_topics = '--'
		name_credits = '--'

		"""
		Determining the step status for the display of the side information.
		As the steps move up, so does the level of information
		"""
		if step == 0:
                    # Sizes for the clodue
                    sizes = ['tiny','small','normal','large','huge']
                    # Get all subjects
                    subjects = [s.name for s in Subject.objects.all()]
                    if request.user.is_authenticated():
                        # If user is authenticated add to the list all subjects she has used
			subjects.extend([s.name for s in Subject.objects.filter(subjectcombination__course__author=request.user)])
                    
                    # Create a subject cloud
                    ctx['subject_cloud'] = cloudify(subjects,sizes)

		if step > 0:
			subjects = SubjectCombination.objects.get(pk=int(request.POST['0-subjects']))
			previous_values.append({'label':u'Námsgreinar','value':markdown(subjects.subjects())})
			name_subjects = subjects.abbreviation

			topics = TopicCombination.objects.get(pk=int(request.POST['0-topics']))
			previous_values.append({'label':u'Viðfangsefni','value':markdown(topics.topics())})
			name_topics = topics.abbreviation

		if step > 1:
			descriptive_name = request.POST['1-descriptive_name']
			previous_values.insert(0, {'label':u'Lýsandi nafn', 'value':markdown(descriptive_name)})

			level = request.POST['1-level']
			previous_values.append({'label':u'Þrep','value':u'<p>%s. þrep</p>' % level})
			name_level = level

			prerequisites = request.POST['1-prerequisites']
			previous_values.append({'label':u'Forkröfur','value':markdown(prerequisites)})

			description = request.POST['1-description']
			previous_values.append({'label':u'Lýsing','value':markdown(description)})

		if step == 3:
			credits = request.POST['2-credits']
			previous_values.insert(4, {'label':u'Framhaldsskólaeiningar', 'value':markdown(u'%s framhaldsskólaeiningar' % credits)})
			name_credits = '%02d' % int(credits)

			knowledge_goals = [Goal.objects.get(pk=int(g.strip())) for g in request.POST.getlist('2-knowledge_goals')]
			previous_values.append({'label':u'Þekkingarviðmið', 'value':u'<ul>%s</ul>' % ' '.join(['<li>%s</li>' % x.goal for x in knowledge_goals])})
			skills_goals = [Goal.objects.get(pk=int(g.strip())) for g in request.POST.getlist('2-skills_goals')]
			previous_values.append({'label':u'Leikniviðmið', 'value':u'<ul>%s</ul>' % ' '.join(['<li>%s</li>' % x.goal for x in skills_goals])})
			competence_goals = [Goal.objects.get(pk=int(g.strip())) for g in request.POST.getlist('2-competence_goals')]
			previous_values.append({'label':u'Hæfniviðmið', 'value':u'<ul>%s</ul>' % ' '.join([u'<li>%s<ul><li><div><em>Námsmat</em></div>%s</li></ul></li>' % (x.goal, ' '.join([u'%s<br/>' % e.evaluation for e in x.evaluation_set.all()])) for x in competence_goals])})
                        ctx['author'] = request.user.get_profile()

		ctx['abbreviation'] = u'%s%s%s%s' % (name_subjects, name_level, name_topics, name_credits)
		ctx['previous_values'] = previous_values

		return super(CourseWizard, self).render_template(request,form,previous_fields,step,ctx)

	"""
	If we are in steps 0 or 2, render their templates, else render the
	default template
	"""
	def get_template(self, step):
		if step == 0:
			return 'curricula/newcourse_subject_topic.html'

		if step == 2:
			return 'curricula/newcourse_goals_credits.html'
                if step == 3:
			return 'curricula/newcourse_evaluation_authors.html'

		return 'curricula/newcourse.html'
