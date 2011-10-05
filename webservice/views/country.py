from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.cache import cache_page
from Frodi.country.models.regions import *
import simplejson as json

def mark(request, area):
	ctx = []

	country_areas = CountryArea.objects.exclude(name=area.capitalize())
	for country_area in country_areas:
		ctx.append({'name':country_area.name,
			    'svg_points':country_area.points,
			    'status':'normal'})

	try:
		country_area = CountryArea.objects.get(name=area.capitalize())
		ctx.append({'name':country_area.name,
			    'svg_points': country_area.points,
			    'status':'highlight'})
	except:
		pass

	return HttpResponse(json.dumps(ctx), mimetype='application/json')


def get(request, area):
	try:
		country_area = CountryArea.objects.get(name=area.capitalize())
		return HttpResponse(json.dumps({'name':country_area.name,
						'svg_points': country_area.points}), mimetype='text/plain')
	except:
		return HttpResponse(json.dumps({}), mimetype='application/json')

def get_all_but_exclude(request, area):
	ctx = []

	country_areas = CountryArea.objects.exclude(name=area.capitalize())
	for country_area in country_areas:
		ctx.append({'name':country_area.name,
			    'svg_points':country_area.points})

	return HttpResponse(json.dumps(ctx), mimetype='application/json')
