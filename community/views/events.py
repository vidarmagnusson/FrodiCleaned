# -*- encoding: utf-8 -*-
from structure.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.contrib.sites.models import Site

from community.models import Event
from community.forms import EventForm

import markdown
import re
import datetime

def event_list(events, request):
	ctx = {'title':'Atburðir á döfinni'}

        ctx['content'] = events
        ctx['formtitle'] = 'Veist þú um eitthvað sem er á döfinni?'
        ctx['formpostto'] = reverse('post-event')
        ctx['form'] = EventForm()

        return ctx

def all(request):
	events = Event.objects.all().order_by('-start_date')
	return render('community/event_list.html', event_list(events,request), request)	

def upcoming(request):
	today = datetime.date.today()
	events = Event.objects.filter(start_date__gte=today).order_by('-start_date')
	return render('community/event_list.html', event_list(events,request), request)	

def single(request, slug):
	events = Event.objects.filter(slug=slug)
	return render('community/event_list.html', event_list(events,request), request)	

@login_required
def new(request):
        if request.method == 'POST':
                form = EventForm(request.POST)
                event = form.save(commit=False)
		event.creator = request.user
                event.save()
                return HttpResponseRedirect('/')

	return render('community/new.html', {'title': 'Nýr viðburður', 'form':EventForm(),}, request)

