from django.forms import ModelForm, Form, TextInput, MultipleHiddenInput
from curricula.forms.widgets import SliderInput, ProfessionInput, CourseSelection, PinnedCourseSelection
from django.shortcuts import render_to_response
from django.contrib.formtools.wizard import FormWizard
from django.http import HttpResponseRedirect

from django.utils.translation import ugettext as _

from structure.utils import cloudify, slugicefy
from curricula.models.programmes import *
from curricula.models.courses import Course
from curricula.models.fields_and_exams import Field, Profession

class ProgrammeForm(ModelForm):
	class Meta:
		model = Programme

class ProgrammeCreateForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProgrammeCreateForm, self).__init__(*args, **kwargs)
		self.fields['profession'].help_text = self.fields['profession'].help_text.replace(_(u'Hold down "Control", or "Command" on a Mac, to select more than one.'), '')
	class Meta:
		model = Programme
		fields = ('profession',)
		widgets={'profession':ProfessionInput()}

class ProgrammeDescriptionForm(ModelForm):
	class Meta:
		model = Programme
		fields = ('title', 'description', 'rights_after_graduation', 'competence_goals')

class ProgrammeOrganizationForm(ModelForm):
	class Meta:
		model = Programme
		fields = ('prerequisites', 'structure', 'training', 'progress_rules', 'quality_assurance')

class ProgrammeCompetenceForm(ModelForm):
	class Meta:
		model = Programme
		fields = ('key_competence_descriptions', 'key_competence_goals')

class ProgrammeEvaluationForm(ModelForm):
	class Meta:
		model = Programme
		fields = ('evaluation', 'grades', 'previous_education')

class ProgrammeCoursesForm(ModelForm):
	def __init__(self, *args, **kwargs):
    		super(ProgrammeCoursesForm, self).__init__(*args, **kwargs)
    		self.fields['credits'].widget.attrs['max'] = kwargs['initial']['maximum_credits']
   		self.fields['credits'].widget.attrs['min'] = kwargs['initial']['minimum_credits']
		self.fields['specialization'].widget.attrs['packages'] = kwargs['initial']['packages']

		self.fields['core'].help_text = self.fields['core'].help_text.replace(_(u'Hold down "Control", or "Command" on a Mac, to select more than one.'), '')
		self.fields['specialization'].help_text = self.fields['specialization'].help_text.replace(_(u'Hold down "Control", or "Command" on a Mac, to select more than one.'), '')
		self.fields['packaged_electives'].help_text = self.fields['packaged_electives'].help_text.replace(_(u'Hold down "Control", or "Command" on a Mac, to select more than one.'), '')
		self.fields['free_electives'].help_text = self.fields['free_electives'].help_text.replace(_(u'Hold down "Control", or "Command" on a Mac, to select more than one.'), '')

	class Meta:
		model = Programme
		fields = ('credits', 'core', 'specialization', 'packaged_electives', 'free_electives')
		widgets = {'credits':SliderInput(attrs={'unit':'fein.'}),
			   'core':CourseSelection(),
			   'specialization':PinnedCourseSelection(),
			   'packaged_electives':CourseSelection(),
			   'free_electives':CourseSelection()}

class ProgrammeWizard(FormWizard):
	def done(self, request, form_list):
		return HttpResponseRedirect('/')

	def process_step(self, request, form, step):
		if step == 0 and hasattr(form, 'cleaned_data'):
			maximum_credits = 0
			minimum_credits = 0
			professions = form.cleaned_data.get('profession')
			for p in professions:
				if (not maximum_credits) or (maximum_credits < p.exam.maximum_credits):
					maximum_credits = p.exam.maximum_credits
				if (not minimum_credits) or (minimum_credits < p.exam.minimum_credits):
					minimum_credits = p.exam.minimum_credits

			if not maximum_credits:
				maximum_credits = 240
			if not minimum_credits:
				minimum_credits = 30

			self.initial[5] = {'credits':minimum_credits,
					   'maximum_credits':maximum_credits,
					   'minimum_credits':minimum_credits,
					   'packages':','.join([p.title for p in professions])}

	def render_template(self, request, form, previous_fields, step, context=None):
		if not context:
			context = {}

		ctx = context
		previous_values = []

		"""
		Determining the step status for the display of the side information.
		As the steps move up, so does the level of information
		"""
		if step == 0:
                    # Sizes for the cloud
                    sizes = ['tiny','small','normal','large','huge']

                    # Get all professions
		    profession_clouds = {}
		    for p in Profession.objects.all():
			    try:
				    profession_clouds[p.exam.title].append(p.title.lower())
			    except:
				    profession_clouds[p.exam.title] = [p.title.lower()]

		    if request.user.is_authenticated():
			    # If user is authenticated add to the list all professions within the same field as the profession she has used
			    fields = Field.objects.filter(subfield__profession__programme__author=request.user)
			    for p in Profession.objects.filter(field__field__in=fields):
				    try:
					    profession_clouds[p.exam.title].append(p.title.lower())
				    except:
					    profession_clouds[p.exam.title] = [p.title.lower()]
			    
			    # Create a profession cloud
			    ctx['exams'] = Exam.objects.all()
			    ctx['levels'] = [_('Level 1'), _('Level 2'), _('Level 3'), _('Level 4'), ]
			    ctx['fields'] = Field.objects.all()
			    ctx['profession_clouds'] = []
			    for exam in profession_clouds.keys():
				  ctx['profession_clouds'].append({'exam':exam, 'cloud':cloudify(profession_clouds[exam],sizes)})

		if step == 3:
			default_competence_values = {}
			default_competences = KeyCompetence.objects.filter(default=True)
			for competence in default_competences:
				 default_competence_values[competence.get_key_competence_display()] = competence.description
 
			ctx['key_competence_fields'] = []
			for (choice_value, choice_title) in KeyCompetence.KEY_COMPETENCE_CHOICES:
				ctx['key_competence_fields'].append({'label_tag':choice_title, 'choice':choice_value, 'name':slugicefy(choice_title), 'value':default_competence_values.get(choice_title,'')})

		if step == 5:
			# Needs a better filter when school approval is up and running
			ctx['courses'] = Course.objects.all()
			
		return super(ProgrammeWizard, self).render_template(request,form,previous_fields,step,ctx)

	def parse_params(self, request, *args, **kwargs):
		for (key,value) in kwargs:
			self.initial[key]=value

	def get_template(self, step):
		if step == 0:
			return 'curricula/newprogramme_profession_title.html'
		if step == 3:
			return 'curricula/newprogramme_key_competences.html'
		if step == 5:
			return 'curricula/newprogramme_courses.html'

		return 'curricula/newprogramme.html'
