# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
from feedzilla.models import Post
from community.models import ActivityEntry
from structure.shortcuts import render
from structure.models import Menu, Slide
from structure.forms import MenuForm, HighlightForm, PartialFlatPageForm, RegisterForm
import markdown

def rss(request):
	return render_to_response('rss/rss.html', {},
                                  context_instance=RequestContext(request))

@login_required
def list_empty(request):
	menu_items = Menu.on_site.all().order_by('url')
	empty = []
	for menu_item in menu_items:
		try:
			match = resolve(menu_item.url)
		except:	
			try:
				FlatPage.objects.get(url=menu_item.url)
			except:
				empty.append({'title':menu_item.title,
					      'url':reverse('modify-page', kwargs={'url':menu_item.url}),})

	return render('management/url_list.html', {'title':'Efnislausar síður' ,'list':empty}, request)

@login_required
def create_flatpage(request, url):
        if request.method == 'POST':
                form = PartialFlatPageForm(request.POST)
		page = form.save(commit=False)
		page.enable_comments = False
		page.registration_required = False
		page.content = markdown.markdown(page.content)
		page.url = url
		page.save()
		page.sites.add(Site.objects.get_current())
		form.save_m2m()

                return HttpResponseRedirect(url)
        
        return render('management/new.html', {'title':'Síðuskrif', 'form':PartialFlatPageForm(),}, request)

@login_required
def create_highlight(request):
        if request.method == 'POST':
                form = HighlightForm(request.POST)
		highlight = form.save(commit=False)
		highlight.order = 0
		highlight.save()
		form.save_m2m()
		
		try:
	                return HttpResponseRedirect(highligt.pages.all()[0])
		except:
			return HttpResponseRedirect('/')
        
        return render('management/new.html', {'title':'Nýr hliðarreitur', 'form':HighlightForm(),}, request)

def welcome(request):
	entries = ActivityEntry.objects.exclude(verb='http://activitystrea.ms/schema/1.0/update').exclude(verb='http://activitystrea.ms/schema/1.0/tag').order_by('-time')[:6]
	return render('welcome.html', {'slides':Slide.objects.all(),
				       'school_feeds':Post.objects.all()[:6],
				       'activity_entries':entries}, request)

def register(request):
        if request.method == 'POST':
                try:
                        form = RegisterForm(request.POST)
                        new_user = form.save()
                        user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password1'))
                        if user is not None and user.is_active:
                                auth.login(request, user)
                                return HttpResponseRedirect('/')
                except:
                        pass

        return render('users/register.html', {'form':RegisterForm()}, request)
