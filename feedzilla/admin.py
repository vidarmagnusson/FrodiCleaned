# -*- coding: utf-8
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from urlparse import urlsplit

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from feedzilla.models import Feed, Post

def html_link(url):
    host = urlsplit(url).hostname
    return u'<a href="%s">%s</a>' % (url, host)


class FeedAdmin(admin.ModelAdmin):
    list_display = ['feed_url', 'last_checked', 
		    'active_post_count', 'post_count', 'created']
    search_fields = ['feed_url']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'created', 'active',
                    'admin_post_link']
    list_filter = ['feed']
    search_fields = ['title', 'link', 'feed__title']

    def admin_post_link(self, obj):
        return html_link(obj.link)

    admin_post_link.short_description = _('Post link')

admin.site.register(Feed, FeedAdmin)
admin.site.register(Post, PostAdmin)
