from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
from structure.shortcuts import render
from structure.utils import cloudify
from community.models import *

def search(request, tagstring=''):
    if request.method == 'GET':
        searchlist = []
        taglist = tagstring.split(' ')
        every_search = Search.objects.filter(tag__tag__in=taglist):
        for search in every_search:
            searchlist.extend([s for s in search.split(' ') if s != ''])

	return render('oer/search.html', {'tags':tagstring, searchcloud=cloudify(searchlist, ['tiny', 'small', 'normal', 'large', 'huge'])}, request)
