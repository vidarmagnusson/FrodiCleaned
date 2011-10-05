# -*- encoding: utf-8 -*-
from structure.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.contrib.sites.models import Site

from community.models import Question, Tag
from community.forms import QuestionForm, AnswerForm

import markdown
import re

def question_list(questions, request):
	ctx = {'title':'Spurningasafn'}
	if Site.objects.get_current().domain == 'hofundarettur.is':
		ctx['title'] = 'Spurningar um höfundarétt'

	ctx['content'] = questions
	ctx['formtitle'] = 'Ert þú með spurningu?'
	ctx['formpostto'] = reverse('post-question')
	ctx['form'] = QuestionForm()

	return ctx

def all(request):
	questions = Question.objects.all().order_by('-created')
	return render('community/question_list.html', question_list(questions,request), request)

def single(request, slug):
        questions = Question.objects.filter(slug=slug)
	return render('community/question_list.html', question_list(questions, request), request)

def by_tag(request, tag):
	questions = Question.objects.filter(tags__slug=tag)
	return render('community/question_list.html', question_list(questions, request), request)

def new(request):
	if request.method == 'POST':
		form = QuestionForm(request.POST)
                question = form.save(commit=False)
		question.creator = request.user
		question.save()
		print question
		return HttpResponseRedirect(reverse('singlequestion', kwargs={'slug':question.slug}))

	return HttpResponseRedirect(reverse('all-questions'))
