from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout
from community.feeds import rss_event

urlpatterns = patterns('',
    url(r'^$', 'community.views.events.upcoming'),

    url(r'^nefndir-rad-og-samtok/$', 'community.views.bookmarks.flatpage_added_organizations'),

    url(r'^hofundalog/$', 'laws.views.view_law'),
    url(r'^hofundalog/(?P<number>.*)/$', 'laws.views.view_law'),

    url(r'^logleg-thjonusta/$', 'community.views.bookmarks.all'),
    url(r'^(?P<tag>[^/]+)/logleg-thjonusta/$', 'community.views.bookmarks.by_tag'),
    url(r'^bua-til/logleg-thjonusta/$', 'community.views.bookmarks.new', name='post-bookmark'),
    url(r'^logleg-thjonusta/(?P<slug>[^/]+)/$', 'community.views.bookmarks.single', name='singlebookmark'),

    url(r'^spurt-og-svarad/$', 'community.views.questions.all', name='all-questions'),
    url(r'^(?P<tag>[^/]+)/spurt-og-svarad/$', 'community.views.questions.by_tag'),
    url(r'^bua-til/spurning/$', 'community.views.questions.new', name='post-question'),
    url(r'^spurning/(?P<slug>[^/]+)/$', 'community.views.questions.single', name='singlequestion'),

    url(r'^rss/?$', rss_event(), name='rss-event'),

    url(r'^a-dofinni/$', 'community.views.events.all', name='all-events'),
    url(r'^a-dofinni/atburdur/(?P<slug>[^/]+)/$', 'community.views.events.single', name='singleevent'),
    url(r'^bua-til/atburdur/$', 'community.views.events.new', name='post-event'),

    url(r'^notendur/innskraning/$', login, {'template_name':'users/login.html'}),
    url(r'^notendur/utskraning/$', logout, {'template_name':'users/logout.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/copyright/'}),
    url(r'^api/community/', include('webservice.community.urls')),
)
