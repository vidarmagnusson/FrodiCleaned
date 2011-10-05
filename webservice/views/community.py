# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from Frodi.community.models import ActivityConstruct, Tag, Comment
from Frodi.country.models.regions import Municipality
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import ugettext as _

import simplejson as json

def tag(request):
	if not request.user.is_authenticated():
		return HttpResponse(json.dumps({'success':False, 'reason':_('User is not authorized to add a tag')}), mimetype='application/json')

	atom_id = request.POST.get('atom', None)
	if atom_id:
		try:
			activity_construct = ActivityConstruct.objects.get(atom_id=atom_id)
		except:
			return HttpResponse(json.dumps({'success':False, 'reason':_('Activity not found')}), mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'success':False, 'reason':_('Activity not specified')}), mimetype='application/json')

	added_tags = []
	for tag in [t.strip() for t in request.POST.get('tag', '').split(',')]:
		if tag != '':
			try:
				tag_object = Tag.objects.get(tag=tag, target=activity_construct)
			except:
				tag_object = Tag.objects.create(tag=tag, target=activity_construct, creator=request.user.get_profile())
				added_tags.append({'tag':tag, 'slug':tag_object.slug})

	return HttpResponse(json.dumps({'success':True, 'tags':added_tags}), mimetype='application/json')


def comment(request):
	if not request.user.is_authenticated():
		return HttpResponse(json.dumps({'success':False, 'reason':_('User is not authorized to add a comment')}), mimetype='application/json')
	atom_id = request.POST.get('atom', None)
	if atom_id:
		activity_construct = ActivityConstruct.objects.get(atom_id=atom_id)
	else:
		return HttpResponse(json.dumps({'success':False, 'reason':_('Activity not found')}), mimetype='application/json')
	content = request.POST.get('comment', '')
	title = content[:64]

	try:
		comment = Comment.objects.create(content=content, creator=request.user.get_profile(), parent=activity_construct, title=title)

		return HttpResponse(json.dumps({'success':True, 'user_avatar':comment.creator.avatar, 'user_name':comment.creator.title.capitalize(), 'user_link':comment.creator.permalink, 'comment':comment.content, 'published':_('just now')}), mimetype='application/json')
	except:
		return HttpResponse(json.dumps({'success':False, 'reason':_('Could not create a comment')}), mimetype='application/json')

def location(request):
	if not request.user.is_authenticated():
		return HttpResponse(json.dumps({'success':False, 'reason':_('User is not authenticated')}), mimetype='application/json')

	postcode = request.GET.get('postcode', None)
	if not postcode:
		return HttpResponse(json.dumps({'success':False, 'reason':_('Postal code not submitted')}), mimetype='application/json')		
	
	try:
		municipality = Municipality.objects.get(postal_code=int(postcode))
	except:
		return HttpResponse(json.dumps({'success':False, 'reason':_('Municipality not found')}), mimetype='application/json')

	user_profile = request.user.get_profile()
	if user_profile.location != municipality:
		user_profile.location = municipality
		user_profile.save()

	return HttpResponse(json.dumps({'success':True, 'municipality':municipality.__unicode__()}), mimetype='application/json')
