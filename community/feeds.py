# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from community.models import Event

import markdown

class rss_event(Feed):
#    def get_object(self, request):
#	return get_object_or_404(Event)

    def title(self, obj):
	return u'Atburðir sem tengast höfundarétti'

    def link(self, obj):
	return reverse('rss-event')

    def description(self, obj):
	return u'Atburðir á döfinni sem snúast um höfundarétt og höfundaréttarlög'

    def items(self, obj):
        return Event.objects.all().order_by('-start_date')[:30]

    def item_link(self,item):
	return reverse('singleevent', kwargs={'event':item.title})

    def item_title(self,item):
	return item.title

    def item_description(self,item):
	if item.end_date:
		return '<p>%s</p><p>%s - %s</p>' % (markdown.markdown(item.description), item.start_date, item.end_date)
	else:
		return '<p>%s</p><p>%s</p>' % (markdown.markdown(item.description), item.start_date)
