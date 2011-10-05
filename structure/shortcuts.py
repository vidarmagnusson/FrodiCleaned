from django.template import RequestContext
from django.shortcuts import render_to_response

def render(template, dictionary, request):
	return render_to_response(template, dictionary, context_instance=RequestContext(request))
