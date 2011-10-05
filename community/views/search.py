from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
from structure.shortcuts import render
from structure.utils import cloudify
from community.models import *

def search(request, tags=''):
    if request.method == 'POST':
        searchstring = request.POST.get('search','')
        searchqueries = [Q(title__icontains=s) for s in searchstring.split(' ')]
        q_query = searchqueries.pop()
        for searchquery in searchqueries:
            q_query |= searchquery

        taglist = [t.strip() for t in request.POST.get('tags','').split(',')]
        results = ActivityConstruct.objects.filter(q_query & Q(tag_set__tag__in=taglist))
        return render('oer/search_results.html', {'search':searchstring, 'tags':tags, 'results':results}, request)

    else:
        searchlist = []
        taglist = [t.strip() for t in tags.split(',')]
        every_search = Search.objects.filter(tag__tag__in=taglist)

        # Create a search cloud
        for search in every_search:
            searchlist.extend([s for s in search.split(' ') if s != ''])

        sizes = ['tiny','small','normal','large','huge']
        searchcloud = cloudify(searchlist, sizes)

        # Bottom feeders
        if request.user.is_authenticated():
            my_search = every_search.filter(searcher=request.user)[:5]
        else:
            my_search = []
        popular_search = every_search[:5]
        newest_content = ActivityEntry.objects.filter(activityobject__tag_set__tag__in=taglist).order_by('-time')[:5]
        print newest_content

	return render('oer/search.html', {'tags':tags, 'searchcloud':searchcloud, 'personal':my_search, 'popular':popular_search, 'activity_entries':newest_content}, request)
