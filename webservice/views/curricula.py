#! -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET, require_POST
from Frodi.curricula.models.courses import *
from Frodi.curricula.models.programmes import *
from Frodi.curricula.models.fields_and_exams import Profession
from structure.utils import cloudify
import simplejson as json
import re

from django.utils.translation import gettext as _

"""
Get a topic cloud based on every subject in a list of subjects and the
topics used by the user in other courses. Size in topic cloud is based 
on topic frequency use by user. If no topics are found it returns a message
advising the user to take care in this uncharted territory. Method fails
gracefully (the kind error message is given no matter what failed)
since it is used for visual improvement and as aid to the user.
Returns a json object:
  { success: True/False (boolean indicating if operation succeeded),
    cloud: If successful, [list of dictionaries {element:"which element",size:"relative size"}]
    message: If not successful (i.e. success:False), a kind error message,
  }

Used for an ajax call to populate a tag cloud on the fly
"""
@require_GET
def topic_cloud(request):
	# Fail message if something goes "boo boo"
	fail_message = _('No topics found for subject. You will setting the guideline for this subject so take care and be responsible.')

	# Get the list of subjects or return error message
	subjects = [s.strip().lower() for s in request.GET.get('subjects','').split(',') if s.strip() != '']
	if not subjects:
		return HttpResponse(json.dumps({'success':False, 'message':fail_message}), mimetype='application/json')

	# Sizes for the cloud
	sizes = ['tiny','small','normal','large','huge']

	# Get topics for all subjects
	# First we create a set so that same topics in different subjects
	# will not affect the impact (which should be based on use by user)
	topics = [t.name for t in Topic.objects.filter(topiccombination__subject__combination__name__in=subjects).distinct()]

	# If user is authenticated add to the list all topics the user has used
	if request.user.is_authenticated():
		topics.extend([t.name for t in Topic.objects.filter(topiccombination__course__author=request.user) if t.name in topics])

	if not topics:
		return HttpResponse(json.dumps({'success':False, 'message':fail_message}), mimetype='application/json')

	cloud = cloudify(topics, sizes)
	return HttpResponse(json.dumps({'success':True, 'cloud':cloud}), mimetype='application/json')

"""
A method to tunnel the request (based on GET or POST) into the right
method. Only here for clarity and avoid a long method with a large part
of it not being used each time.

Used to be able to to a GET and a POST request based on the same url
"""
def abbreviations(request):
	if request.method == 'GET':
		return get_abbreviations(request)
	elif request.method == 'POST':
		return create_abbreviations(request)

	return HttpResponse('', mimetype='text/plain')


"""
Get an abbreviation for a subject or a list of subjects (comma separated)
as well as for a topic or a list of topics (also comma separated).
Returns a json object:
  { subject_id: Subject combination id (if subject combination is found),
    topic_id: Topic combination id (if topic combination is found),
    subject_abbreviation: Subject abbreviation (if subject combination is found),
    topic_abbreviation: Topic abbreviation (if topic combination is found)
    subjects_found: [List of the subjects in the subject combination that exist],
    subjects_not_found: [List of the subjects in the subject combination that do not exist],
    topics_found: [List of the topics in the topic combination that exist]
    topics_not_found: [List of the topics in the topic combination that do not exist]
    topic_suggestions: [List of topic suggestions as dictionaries: {abbrevation:string, topics:[string list]}]
  }

Used to get abbreviations for subjects and topics and if no abbreviation is found 
list the subjects and topics that do not exist (e.g. to show probable spelling errors)
If the topic is not found list the possible abbreviations (i.e. used for other subjects)
"""
@require_GET
def get_abbreviations(request):
	subjects = request.GET.get('subjects', None)
	topics = request.GET.get('topics', None)

	# Get subjects and topics parameters or return an error message
	if not (subjects and topics):
		return HttpResponse(_('Both subjects and topics must be provided'), mimetype='text/plain')
	
	# Split parameters into a list of lowercased subject/topic names
	subjects = [s.strip().lower() for s in subjects.split(',') if s.strip() != '']
	topics = [t.strip().lower() for t in topics.split(',') if t.strip() != '']

	# Init variables used
	json_return = {'subjects_found':[], 'subjects_not_found':[],
		       'topics_found':[], 'topics_not_found':[]}

	available_subjects = set([])
	available_topics = set([])

	# For every subject in list get the corresponding Subject object and
	# add to a list of available subjects. If it fails add the subject to
	# a list of non existing subjects
	for subject in subjects:
		try:
			subject_object = Subject.objects.get(name=subject)
			# We add to both the available and the result since
			# we need a serializable list for the json return and
			# a Subject object to find a subject combination
			available_subjects.add(subject_object)
			json_return['subjects_found'].append(subject)
		except:
			json_return['subjects_not_found'].append(subject)

	# Do the same for topics, i.e. get a list of Topic objects and mark
	# whether topics were found or not
	for topic in topics:
		try:
			topic_object = Topic.objects.get(name=topic)
			available_topics.add(topic_object)
			json_return['topics_found'].append(topic)
		except:
			json_return['topics_not_found'].append(topic)

	# Try to get the subject and topic combinations but only if
	# all subjects and topics were found
	subject_combination = None
	topic_combination = None

	if not json_return['subjects_not_found']:
		subject_combination = subjectcombination_find_by_set(available_subjects)
	if not json_return['topics_not_found']:
		topic_combination = topiccombination_find_by_set(available_topics, subject_combination)

	# If a subject combination is found, add the id and the abbreviation
	if subject_combination:
		json_return['subject_id'] = subject_combination.id
		json_return['subject_abbreviation'] = subject_combination.abbreviation

	# If a topic combination is found, add id and abbreviation, if not add
	# suggestions based on each topic
	if topic_combination:
		json_return['topic_id'] = topic_combination.id
		json_return['topic_abbreviation'] = topic_combination.abbreviation
	else:
		json_return['topic_suggestions'] = topiccombination_find_any(available_topics)

	return HttpResponse(json.dumps(json_return),
			    mimetype='application/json')


"""
Create abbreviation for a subject or a list of subjects (comma separated) and for
topics (or a comma separated list of topics). If abbreviation exists already the
old abbreviation is used (never overwritten). Assumes that a topic combination is
always connected to a subject combination (the same abbreviation can mean different
things for different subject abbreviations)

Returns a json object:
  { success: True/False (boolean indicating if operation succeeded),
    subject_id: If successful (i.e. success:True), id of the new subject abbreviation,
    topic_id: If successful, id of the new topic abbreviation
    reason: If not successful (i.e. success:False), the reason of failure,
    origin: Indicates whether the source of a problem is subjects or topics (subjects|topics)
  }

Used to create new abbreviations for subject and topic combinations and create all
*participating* subjects/topics in the combinations respectively)
"""
@require_POST
def create_abbreviations(request):
	user = request.user
	#  User must have permission to add subjects and combination
	if not user.has_perms(['curricula.add_subjectcombination', 'curricula.add_subject']):
		return HttpResponse(json.dumps({'success':False, 'origin':'subjects', 'reason':_('User does not have permission')}), mimetype='application/json')

	# Get stripped, lowercase subjects and topics (exclude empty strings)
	subjects = [s.strip().lower() for s in request.POST.get('subjects-list').split(',') if s.strip() != '']
	topics = [t.strip().lower() for t in request.POST.get('topics-list').split(',') if t.strip() != '']

	# Get subject abbreviation and check that it consists of 4 letters
	subject_abbreviation = request.POST.get('subjects-abbreviation','')
	if not re.match(u'^[a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ]{4}$', subject_abbreviation):
		return HttpResponse(json.dumps({'success':False, 'origin':'subjects', 'reason':_('Abbreviation must be %d characters') % 4}), mimetype='application/json')

	# Get topic abbreviation and check that it consists of 2 letters
	topic_abbreviation = request.POST.get('topics-abbreviation','')
	if not re.match(u'^[a-zA-ZáðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ]{2}$', topic_abbreviation):
		return HttpResponse(json.dumps({'success':False, 'origin':'topics', 'reason':_('Abbreviation must be %d characters') % 2}), mimetype='application/json')	
	
	# Create subject/topic object holders (used to check for existing combinations/abbreviations etc.)
	subjects_in_combination = set([])
	topics_in_combination = set([])

	# Make sure all subjects exist (create one if it doesn't)
	for subject in subjects:
		subject_object, created = Subject.objects.get_or_create(name=subject,defaults={'author':user})
		subjects_in_combination.add(subject_object)

	# Make sure all topics exist (create one if it doesn't)?
	for topic in topics:
		topic_object, created = Topic.objects.get_or_create(name=topic, defaults={'author':user})
		topics_in_combination.add(topic_object)

	# Does the subject combination already exist?
	subject_combination = subjectcombination_find_by_set(subjects_in_combination)

	# If the subject combination does not exist it must be created
	if not subject_combination:
		# Is abbreviation free?
		if not subject_abbreviation_free(subject_abbreviation):
			return HttpResponse(json.dumps({'success':False, 'origin':'subjects', 'reason':_('Abbreviation is already in use by another subject combination')}), mimetype='application/json')

		# Create a new subject combination with the abbreviation and subjects
		subject_combination = SubjectCombination.objects.create(abbreviation=subject_abbreviation, author=user)
		# Add the subjects to the new subject combination
		for subject in subjects_in_combination:
			subject_combination.combination.add(subject)
		subject_combination.save()

		# If we just created the subject combination, then the topic combination does not exist
		topic_combination = None
	else:
		# Check for topic combination in the same way as we did when we found the subject combination
		topic_combination = topiccombination_find_by_set(topics_in_combination, subject_combination)

	# If the topic combination is not found, it must be created
	if not topic_combination:
		# Is abbreviation free?
		if not topic_abbreviation_free(topic_abbreviation, subject_combination):
			return HttpResponse(json.dumps({'success':False, 'origin':'topics', 'reason':'Skammstöfun er notuð af öðrum viðfangsefnum.'}), mimetype='application/json')

		# Create a new topic combination with the abbreviation, topics and the subject combination
		topic_combination = TopicCombination.objects.create(abbreviation=topic_abbreviation, subject=subject_combination, author=user)
		
		# Add the topics to the new topic combination
		for topic in topics_in_combination:
			topic_combination.combination.add(topic)
		topic_combination.save()

	return HttpResponse(json.dumps({'success':True, 'subject_id':subject_combination.id, 'topic_id':topic_combination.id}), mimetype='application/json')

"""
Creates a new goal given that the user has permission and sets the user as its 
author. If an evaluation is provided (i.e. evaluation is not absent or an empty string)
it is added to the goal along with the author (also given that the user has permission).

Returns a json object:
  { success: True/False (boolean indicating if operation succeeded),
    goal_id: If successful (i.e. success:True), id of the new goal,
    evaluation_id: If successful and evaluation provided, id of the new evaluation
    reason: If not successful (i.e. success:False), the reason of failure,
  }

Used to create a new goal and evaluation in one go
"""
@require_POST
def create_goal(request):
	# Get the goal provided and return an error message if not found
        posted_goal = request.POST.get('goal', None)
	if not posted_goal:
		return HttpResponse(json.dumps({'success':False, 'reason':_('No goal provided')}), mimetype='application/json')

	# User must have permission to add goals and evaluations
	if request.user.has_perms(['curricula.add_goal', 'curricula.add_evaluation']):
		# Create goal and add the user as its author
		goal = Goal.objects.create(goal=posted_goal)
		goal.author.add(request.user)
		goal.save()

		# Create the return dictionary (so evaluation can possibly be added)
		return_json = {'success':True, 'goal_id':goal.id}
		
		# Try to get the evaluation
		posted_evaluation = request.POST.get('evaluation', '')
		if posted_evaluation != '':
			# If evaluation is not an empty string create it, link it to the goal
			# and add the user as its author
			evaluation = Evaluation.objects.create(goal=goal, evaluation=posted_evaluation)
			evaluation.author.add(request.user)
			evaluation.save()
			# Add the evaluation to the return dictionary
			return_json['evaluation_id'] = evaluation.id

		return HttpResponse(json.dumps(return_json), mimetype='application/json')

	else:
		# If user does not have the permission
		return HttpResponse(json.dumps({'success':False, 'reason':_('Not authorized to create goal')}), mimetype='application/json')

"""
Delete a goal given that the user has permissions to delete a goal.
Returns a json object:
  { success: True/False (boolean indicating if operation succeeded),
    reason: If not successful (i.e. success:False), the reason of failure,
  }

Simple method used to delete goals (and corresponding evaluations)
"""
@require_POST
def delete_goal(request):
	# Try to find the correct goal object based on the id given
	goal_id = request.POST.get('goal','')
	try:
		goal = Goal.objects.get(id=int(goal_id))
	except:
		return HttpResponse(json.dumps({'success':False, 'reason':_('Goal not found')}), mimetype='application/json')

	# User must be allowed to delete both goals and evaluations (which can be linked to goals)
	if request.user.has_perms(['curricula.delete_goal', 'curricula.delete_evaluation']):
		# If user is authorised, delete the goal and return success
		goal.delete()
		return HttpResponse(json.dumps({'success':True}), mimetype='application/json')
	else:
		# Return with authorisation failure
		return HttpResponse(json.dumps({'success':False, 'reason':_('Not authorized to delete goals')}), mimetype='application/json')

def get_professions(request):
	# Get the list of professions
	professions = request.GET.get('professions', None)

	# Get subjects and topics parameters or return an error message
	if not (professions):
		return HttpResponse(json.dumps({'success':False, 'reason':_('No professions provided')}), mimetype='application/json')
	
	# Split parameters into a list of lowercased subject/topic names
	professions = [p.strip().lower() for p in professions.split(',') if p.strip() != '']

	# Init variables used
	# We assume at this point that it will be successful and that we find
	# all professions
	json_return = {'success':True, 'found_all':True, 'professions_found':[], 'professions_not_found':[]}
	
	# Loop through the professions list and get the professions (put them
	# in either found or not found based on if they existed or not)
	for profession in professions:
		try:
			profession_object = Profession.objects.get(title=profession)
			# We add the profession as an available profession
			json_return['professions_found'].append({'id':profession_object.id, 'title':profession_object.title})
		except:
			json_return['professions_not_found'].append(profession)

	# If there are any professions not found, we add a found_all=False
	if json_return['professions_not_found']:
		json_return['found_all'] = False

	return HttpResponse(json.dumps(json_return), mimetype='application/json')

@require_POST
def create_key_competence_goal(request):
	# Get the goal provided and return an error message if not found
        competence_goal = request.POST.get('goal', None)
	competence_choice = request.POST.get('key_competence_choice', None)

	if not competence_goal or not competence_choice:
		return HttpResponse(json.dumps({'success':False, 'reason':_('Both competence description and competence type (number) must be provided')}), mimetype='application/json')

	# User must have permission to add goals and evaluations
	if request.user.has_perms(['curricula.add_keycompetencegoal']):
		try:
			# Create goal
			goal = KeyCompetenceGoal.objects.create(goal=competence_goal, key_competence=int(competence_choice), author=request.user)
			goal.save()

			return HttpResponse(json.dumps({'success':True, 'goal_id':goal.id}), mimetype='application/json')
		except:
			return HttpResponse(json.dumps({'success':False, 'reason':_('Unable to create competence goal')}), mimetype='application/json')

	else:
		# If user does not have the permission
		return HttpResponse(json.dumps({'success':False, 'reason':_('Not authorized to create competence goal')}), mimetype='application/json')

@require_POST
def delete_key_competence_goal(request):
	# Try to find the correct goal object based on the id given
	goal_id = request.POST.get('goal','')
	try:
		goal = KeyCompetenceGoal.objects.get(id=int(goal_id))
	except:
		return HttpResponse(json.dumps({'success':False, 'reason':_('Goal not found')}), mimetype='application/json')

	# User must be allowed to delete both goals and evaluations (which can be linked to goals)
	if request.user.has_perms(['curricula.delete_goal']):
		# If user is authorised, delete the goal and return success
		goal.delete()
		return HttpResponse(json.dumps({'success':True}), mimetype='application/json')
	else:
		# Return with authorisation failure
		return HttpResponse(json.dumps({'success':False, 'reason':_('Not authorized to delete goals')}), mimetype='application/json')

# This should probably be post since it creates a new key competence if
# it is not found. We let this stay like this for now.
@require_GET
def get_key_competence_id(request):
	# Get the choice and the description
	competence_choice = request.GET.get('choice', None)
	competence_description = request.GET.get('description', '')

	# IF we do not have the choice we fail
	if not competence_choice:
		return HttpResponse(json.dumps({'success':False, 'reason':_('Choice of competence not supplied')}), mimetype='application/json')
	
	if competence_description == '':
		try:
			competence = KeyCompetence.objects.get(key_competence=competence_choice, default=True)
		except:
			return HttpResponse(json.dumps({'success':False, 'reason':_('Key competence description not found')}), mimetype='application/json')
	else:
		try:
			competence = KeyCompetence.objects.get(key_competence=competence_choice, description=competence_description)
		except:

			# If user is allowed to create a new key competence
			# description, create it, else return failure
			if request.user.has_perms(['curricula.add_keycompetence']):
				competence = KeyCompetence.objects.create(key_competence=competence_choice, description=competence_description, author=request.user)
			else:
				return HttpResponse(json.dumps({'success':False, 'reason':_('User not authorized to create key competence descriptions')}), mimetype='application/json')

	return HttpResponse(json.dumps({'success':True, 'competence_id':competence.id}), mimetype='application/json')


@require_POST
def create_course_package_goal(request):
	# Get the goal provided and return an error message if not found
        title = request.POST.get('title', None)
	initial_course = request.POST.get('course', None)

	if not title:
		if initial_course:
			title = initial_course.id_name()
		else:
			title = _('New Course Package')

	# User must have permission to add goals and evaluations
	if request.user.has_perms(['curricula.add_course_package']):
		try:
			# Create goal
			package = CoursePackage.objects.create(title=title, author=request.user)
			package.courses.add(initial_course)
			package.save()

			return HttpResponse(json.dumps({'success':True, 'package_id':package.id}), mimetype='application/json')
		except:
			return HttpResponse(json.dumps({'success':False, 'reason':_('Unable to create course package')}), mimetype='application/json')

	else:
		# If user does not have the permission
		return HttpResponse(json.dumps({'success':False, 'reason':_('Not authorized to create course package')}), mimetype='application/json')

"""
Not implemented
"""
@require_POST
def update_course_package(request):
	pass
