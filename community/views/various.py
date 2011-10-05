from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from structure.shortcuts import render
from community.models import *
from community.forms import *
import datetime
import re

def index(request, username=None, construct=None):
	entries = ActivityEntry.objects.all()
	constructs = []
	if construct:
		if construct == 'notes':
			entries = entries.filter(activityobject__in=Note.objects.all())
		elif construct == 'articles':
			entries = entries.filter(activityobject__in=Article.objects.all())
		elif construct == 'photos':
			entries = entries.filter(activityobject__in=Photo.objects.all())
		if construct == 'videos':
			entries = entries.filter(activityobject__in=Video.objects.all())
		elif construct == 'audio':
			entries = entries.filter(activityobject__in=Audio.objects.all())
		elif construct == 'bookmarks':
			entries = entries.filter(activityobject__in=Bookmark.objects.all())
		elif construct == 'files':
			entries = entries.filter(activityobject__in=File.objects.all())
		else:
			pass

	vieweduser=request.user

	if username:
		try:
			vieweduser = User.objects.get(username=username)
			entries = entries.filter(actor=vieweduser.get_profile())
		except:
			pass

	# Events - why 10? I also have idea
	today = datetime.date.today()
	events = Event.objects.filter(start_date__gte=today).order_by('-start_date')[:10]

	# Nor do I have idea why 25 is the magic number
	sortable_list = [e for e in entries.exclude(verb='http://activitystrea.ms/schema/1.0/update').order_by('-time')[:25]]
	if request.user.is_authenticated():
		sortable_list.sort(lambda a,b: -1*cmp(a.activityobject.updated if a.actor == request.user.get_profile() else a.time, b.activityobject.updated if b.actor == request.user.get_profile() else b.time))

	return render('community/timeline.html', {'vieweduser':vieweduser, 'content':sortable_list, 'events':events}, request)

def new(request):
	title = request.POST.get('title',[])
	content = request.POST.get('content',[])
	target = request.POST.get('group', None)
	tags = [t.strip() for t in request.POST.get('tags',[]).split(',') if t.strip() != '']

	# What's the best way to manage licenses?
	license = request.POST.get('license', [])
	if license:
		cc = License.objects.get(id=license)
	else:
		cc = None

	author = request.POST.get('author',
				  request.user.get_profile().title)
	files = request.POST.get('file')

	if files:
		# Not fully implemented
		return HttpResponseRedirect('/')

	if re.match('^(http|https)://(\\w+\\.){1,}\\w+(:\\d+)*/\\S*\\s*$', title):
		bookmark = Bookmark(target_url=title,
				    description=content,
				    creator=request.user.get_profile())
		bookmark.save(target=target)

		for tag in tags:
			tag_object, new_tag = Tag.objects.get_or_create(tag=tag, creator=request.user.get_profile(), target=bookmark)
		return HttpResponseRedirect('/')

	if not content:
		# Create a note and be sure the note is not longer than 
		# 140 characters (should this be configurable?)
		note = Note(content=title[:140],
			    creator=request.user.get_profile(),
			    license=cc)
		note.save(target=target)
		return HttpResponseRedirect('/')
	
	print u'New Article'
      	return HttpResponseRedirect('/')

def personal(request, username):
	try:
		user = User.objects.get(username=username)
		# Why 25? - I have no idea -- need pagination?
		entries = ActivityEntry.objects.filter(actor=user.get_profile()).order_by('-time')[:25]
	except:
		entries = ActivityEntry.objects.all().order_by('-time')[:25]

	# Events - why 10? I also have no idea
	today = datetime.date.today()
	events = Event.objects.filter(start_date__gte=today).order_by('-start_date')[:10]
	return render('community/timeline.html', {'content':entries, 'events':events}, request)

def friends(request, username):
	try:
		user = User.objects.get(username=username)
		following = user.get_profile().following		
		# Why 25? - I have no idea -- need pagination?
		entries = ActivityEntry.objects.filter(Q(actor__in=following.all())|Q(activityobject__in=following.all())|Q(target__in=following.all())).order_by('-time')[:25]
	except:
		entries = ActivityEntry.objects.all().order_by('-time')[:25]

	# Events - why 10? I also have no idea
	today = datetime.date.today()
	events = Event.objects.filter(start_date__gte=today).order_by('-start_date')[:10]
	return render('community/timeline.html', {'content':entries, 'events':events}, request)

@login_required
def mark_like(request):
	if request.method == 'POST':
		try:
			atom_id = request.POST.get('activityobject')
			construct = ActivityConstruct.objects.get(atom_id=atom_id)
			me = request.user.get_profile()
			# Add to favorites (we don't use favorites)
			me.favorites.add(construct)
			me.save()

			# Create activity entry
			me.mark_as_like(construct)
		except:
			pass

	return HttpResponseRedirect('/')

@login_required
def share(request):
	if request.method == 'POST':
		try:
			atom_id = request.POST.get('activityobject')
			construct = ActivityConstruct.objects.get(atom_id=atom_id)
			# Create activity entry
			request.user.get_profile().share(construct)
		except:
			pass

	return HttpResponseRedirect('/')

@login_required
def follow(request):
	if request.method == 'POST':
		try:
			atom_id = request.POST.get('person')
			person = Person.objects.get(atom_id=atom_id)

			# Put into list of following
			me = request.user.get_profile()
			me.following.add(person)
			me.save()

			person.followers.add(me)
			person.save()

			# Create activity entry
			me.start_following(person)
		except:
			pass

	return HttpResponseRedirect('/')

def show_entry(request, entry):
	construct = ActivityConstruct.objects.get(atom_id=entry)
	return render('community/entry.html', {'entry':construct}, request)

def list_private_messages(request, postbox='all'):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		profile = request.user.get_profile()
	
	if postbox == 'outbox':
		outbox = PrivateMessage.objects.filter(sender=profile)
		inbox = None
	elif postbox == 'inbox':
		inbox = PrivateMessage.objects.filter(recipient=profile)
		outbox = None
	else:
		inbox = PrivateMessage.objects.filter(recipient=profile)
		outbox = PrivateMessage.objects.filter(sender=profile)

	return render('community/private_messages.html', {'inbox':inbox, 'outbox':outbox}, request)

def my_person(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	profile = request.user.get_profile()
	if request.method == 'POST':
		profile_form = PersonForm(request.POST, instance=profile)
		if profile_form.is_valid():
			profile_form.save()
		else:
			print profile_form._errors
			render('community/my_person.html', {'profile':profile, 'form':profile_form}, request)	
	else:
		profile_form = PersonForm(instance=profile)

	return render('community/my_person.html', {'profile':profile, 'form':profile_form}, request)

def create_group(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if request.method == 'POST':
		form = GroupForm(request.POST)
		if form.is_valid():
			group = form.save(commit=False)
			group.creator = request.user.get_profile()
			group.avatar = 'http://mrn.pagekite.me/media/icons/groups.jpg'
			group.save()
			request.user.get_profile().groups.add(group)
			return HttpResponseRedirect('/')
	else:
		form = GroupForm()

	return render('community/form.html', {'title':'Create a new group', 'form':form}, request)
	
def list_groups(request):
	return render('community/groups.html', {'groups':Group.objects.all()}, request)

def group(request, group_id):
	try:
		group = Group.objects.get(atom_id=group_id)
	except:
		return list_groups(request)

	group_activities = ActivityEntry.objects.filter(target=group)[:25]

	return render('community/group.html', {'group':group, 'groupactivities':group_activities}, request)

def join_group(request):
	if not request.user.is_authenticated() or not request.method == 'POST':
		return HttpResponseRedirect('/')

	group_id = request.POST.get('group', None)
	if group_id:
		try:
			group = Group.objects.get(atom_id=group_id)

			person = request.user.get_profile()
			person.groups.add(group)
			person.join(group)

			group_activities = ActivityEntry.objects.filter(target=group)[:25]
			return render('community/group.html', {'group':group, 'groupactivities':group_activities}, request)
		except:
			pass

	return HttpResponseRedirect('/')

def leave_group(request):
	if not request.user.is_authenticated() or not request.method == 'POST':
		return HttpResponseRedirect('/')

	group_id = request.POST.get('group', None)
	if group_id:
		try:
			group = Group.objects.get(atom_id=group_id)
			person = request.user.get_profile()
			person.groups.remove(group)
			person.join(group)
		except:
			pass

	return HttpResponseRedirect('/')
