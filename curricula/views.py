# -*- coding: utf-8 -*-
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

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from structure.shortcuts import render
from curricula.forms.programmes import ProgrammeForm
from curricula.forms.stakeholders import StakeholderForm
from curricula.models.extra_information import Stakeholder
from curricula.models.courses import Course, ExemplaryCourse
from curricula.models.fields_and_exams import Exam, Field, Profession
from curricula.forms.courses import ExemplaryCourseForm

from django.utils.translation import ugettext as _

@login_required
def new_programme(request):
	ctx = {'title':'Ný braut', 'form': ProgrammeForm()}
	return render("curricula/newprogramme.html", ctx,request)

@login_required
def new_stakeholder(request):
	if request.method == 'POST':
		form = StakeholderForm(request.POST)
		stakeholder = form.save()

		return HttpResponseRedirect(reverse('stakeholder', kwargs={'slug':stakeholder.slug}))

	ctx = {'title':'Nýr hagsmunaaðili', 'form': StakeholderForm()}
	return render('curricula/stakeholder_new.html', ctx, request)

def stakeholder_list(request):
	return render ('curricula/stakeholders.html', {'stakeholders':Stakeholder.objects.all()}, request)

def stakeholder(request,slug):
	stakeholder = get_object_or_404(Stakeholder, slug=slug)
	return render('curricula/stakeholder.html', {'stakeholder':stakeholder}, request)

"""
Displays all unapproved courses for a user with approve courses priviliges to 
approve.

@todo:  Create a more complex filter, so that only the courses for his school 
are displayed
"""
def unapproved_courses(request):
	if request.user.is_authenticated() and request.user.has_perm('approve_course'):
		courses = Course.objects.filter(status=2)
		return render('curricula/course_list.html', {'courses':courses}, request)
	
	return HttpResponseRedirect('/')

"""
Displays the course in a html-template for the user to approve or reject.  If the course is approved, it goes into the queue for the government to approve, if rejected, it will appear in the author list as a rejected-by-school course.

@author:  Hilmar Kári Hallbjörnsson (isProject)
"""
@login_required
def approve_course(request, author, course):
	if request.method == 'POST' and request.user.is_authenticated():
		unique_id = request.POST.get('unique-id')
		try:
			course = Course.objects.get(unique_id__exact=unique_id)
			if request.user.has_perm('approve_course'):
				if 'approve' in request.POST:	
					msg = u'Tókst að samþykkja áfanga'
					course.status = 3
					course.save()
				elif 'not-approved' in request.POST:
					msg = u'Áfanganum var hafnað'
					course.status = 5
					course.save()
			else:
				msg = u'Þú hefur ekki heimild til að samþykkja þennan áfanga'
		except Exception as details:
			msg = u'Tókst ekki að samþykkja áfanga. Hafið samband við kerfisstjóra'
			
		return_site = {'name':u'Samfélag', 'url':'/'}
		return render('message.html', {'msg':msg, 'return_site':return_site}, request)
	else:
		# Enough to get the first one
		user = author.split('-')[0]
		user_object = get_object_or_404(User, username=user)
		course_object = get_object_or_404(Course, author=user_object, name=course.upper())
		return render('curricula/approve_course.html', {'course':course_object}, request)

"""
Displays the course in a html-template with a button for the user to confirm that he wants to publish the course.
Checks to see if the user is in fact one of the authors and if so, saves the status of the course.
"""
@login_required
def publish_course(request, author, course):
	if request.method == 'POST' and request.user.is_authenticated():
		unique_id = request.POST.get('unique-id')
		try:
			course = Course.objects.get(unique_id__exact=unique_id)
			if request.user in course.author.all():
				me = request.user.get_profile()
				#post_course(me,course)
					
				msg = u'Tókst að birta áfanga'
				course.status = 2
				course.save()
			else:
				msg = u'Þú hefur ekki heimild til að birta þennan áfanga'
		except Exception as details:
			msg = u'Tókst ekki að birta áfanga. Hafið samband við kerfisstjóra'
			
		return_site = {'name':u'Samfélag', 'url':'/'}
		return render('message.html', {'msg':msg, 'return_site':return_site}, request)
	else:
		# Enough to get the first one
		user = author.split('-')[0]
		user_object = get_object_or_404(User, username=user)
		course_object = get_object_or_404(Course, author=user_object, name=course.upper())
		return render('curricula/publish_course.html', {'course':course_object}, request)

def view_course(request, id):
	course = get_object_or_404(Course, unique_id=id)
	if course.status == 1 and request.user != course.author:
		course = None
	
	if course:
		return render('curricula/course.html', {'course':course}, request)
	else:
		return HttpResponseRedirect('/')

"""
Deletes a course
"""
@login_required
def delete_course(request, id):
	if request.method == 'POST' and request.user.is_authenticated():
		if request.POST.get('unique-id'):
			try:
				course = Course.objects.get(unique_id__exact=id)
				if request.user in course.author.all():
					#course.delete()
					msg = _('Successfully deleted course')
				else:
					msg = _('You are not authorized to delete course')
			except:
				msg = _('Course not found')

			return_site = {'name':_('My courses'), 'url':reverse('my-courses')}
			return render('message.html', {'msg':msg, 'return_site':return_site}, request)

	else:
		course = get_object_or_404(Course, unique_id__exact=id)
		return render('curricula/delete_course.html', {'course':course}, request)

"""
Displays all courses that belong to the user:  In Progress, Waiting for School Approval, Waiting for Government Approval,
Approved by the Government, Rejected by the School and Rejected by the Government.  Each status is rendered seperatly in the template
"""
@login_required	
def my_courses(request):
	if request.user.is_authenticated():
		courses = Course.objects.filter(author=request.user).order_by('status')
		return render('curricula/course_list.html',{'courses':courses},request)
	return HttpResponseRedirect('/')

def list_exams(request):
	return render('curricula/exam_list.html', {'exams':Exam.objects.all().order_by('level','title')}, request)

def list_fields(request):
	return render('curricula/field_list.html', {'fields':Field.objects.all()}, request)

def list_professions(request):
	return render('curricula/profession_list.html', {'professions':Profession.objects.all()}, request)

"""
If a course is rejected by either the school or the government, the user can re-activate the course, and store it in in-progress status.
"""
@login_required
def reactivate_course(request, author, course):
	if request.method == 'POST' and request.user.is_authenticated():
		unique_id = request.POST.get('unique-id')
		try:
			course = Course.objects.get(unique_id__exact=unique_id)
			if request.user in course.author.all():
				msg = u'Tókst að endurvekja áfanga'
				course.status = 1
				course.save()
			else:
				msg = u'Þú hefur ekki heimild til að endurvekja þennan áfanga'
		except Exception as details:
			msg = u'Tókst ekki að endurvekja áfanga. Hafið samband við kerfisstjóra'
			
		return_site = {'name':u'Samfélag', 'url':'/'}
		return render('message.html', {'msg':msg, 'return_site':return_site}, request)
	else:
		# Enough to get the first one
		user = author.split('-')[0]
		user_object = get_object_or_404(User, username=user)
		course_object = get_object_or_404(Course, author=user_object, name=course.upper())
		return render('curricula/reactivate_course.html', {'course':course_object}, request)

"""
Displays the course in a html-template with a button for the user to confirm that he wants to publish the course.
Checks to see if the user is in fact one of the authors and if so, saves the status of the course.

@author:  Hilmar Kári Hallbjörnsson (isProject)
"""
@login_required
def make_exemplary_course(request, id):
	if request.method == 'POST' and request.user.is_authenticated():
		try:
			course = Course.objects.get(unique_id__exact=id)
			if request.user.has_perms(['curricula.can_add_exemplarycourse']):
				form = ExemplaryCourseForm(request.POST)
				form.save()
				msg = _('Course has been made into an exemplary course')
			else:
				msg = _('User is not authorized to make this course exemplary')

		except Exception as details:
			msg = _('Course could not be made exemplary. Contact system administrator.')
			
		return_site = {'name':u'Fyrirmyndaráfangar', 'url':reverse('adminlist-exemplary-courses')}
		return render('message.html', {'msg':msg, 'return_site':return_site}, request)
	else:
		course_object = get_object_or_404(Course, unique_id__exact=id)
		return render('curricula/make_course_exemplary.html', {'course':course_object}, request)

def view_exemplary_course(request, id):
	try:
		exemplary = ExemplaryCourse.objects.get(course__unique_id=id)
		return render('curricula/view_exemplary_course.html', {'exemplary':exemplary}, request)
	except:
		return_site = {'name':u'Fyrirmyndaráfangar', 'url':reverse('list-exemplary-courses')}
		return render('message.html', {'msg':'Exemplary course not found', 'return_site':return_site}, request)

def list_exemplary_courses(request):
	if request.user.has_perms(['curricula.can_add_exemplarycourse']):
		courses = Course.objects.filter(status=4).exclude(exemplarycourse__isnull=False)
	else:
		courses = None
	return render('curricula/exemplary_list.html', {'exemplary':ExemplaryCourse.objects.all(), 'courses':courses}, request)
