# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout, password_change, password_change_done
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    url(r'^notendur/innskraning/$', login, {'template_name':'users/login.html'}, name='user-login'),
    url(r'^notendur/utskraning/$', logout, {'template_name':'users/logout.html'}),
    url(r'^notendur/nyskraning/$', 'structure.views.register', name='user-register'),
    url(r'^notendur/lykilord/breyta/$', password_change, {'template_name':'users/password_change.html'}, name='change-password'),
    url(r'^notendur/lykilord/breytt/$', password_change_done, {'template_name':'users/password_change_done.html'}),

    url(r'^menntaefni/$', 'community.views.search.search', kwargs={'tags':'menntaefni'}),
    url(r'^grunngogn/$', 'community.views.search.search', kwargs={'tags':'grunngögn'}),
    url(r'^samfelag/', include('community.urls.community')),
    url(r'^namskrargrunnur/', include('curricula.urls')),
    url(r'^namskrargrunnur/raduneytisstjornbord/hagsmunaadilar/nyr-hagsmunaadili/$', 'curricula.views.new_stakeholder'),
    url(r'^namskrargrunnur/raduneytisstjornbord/hagsmunaadilar/allir-hagsmunaadilar/$', 'curricula.views.stakeholder_list', name='stakeholder'),
    url(r'^namskrargrunnur/raduneytisstjornbord/hagsmunaadilar/hagsmunaadili/(?P<slug>[^/]+)/$', 'curricula.views.stakeholder', name='stakeholder'),
    url(r'^wiki/$', redirect_to, {'url': 'http://wiki.menntagatt.is/'}),
    url(r'^stjornbord/', include('structure.urls')),

    url(r'^nam-og-skolar/', include('schools.urls')),

    url(r'^throun-menntagattar/$', 'feedback.views.list_feedbacks', name='feedback-list'),
    url(r'^throun-menntagattar/athugasemd/(?P<feedback>\d+)/$', 'feedback.views.comment_on_feedback', name='feedback-comment'),
    url(r'^api/', include('webservice.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/'}),
    url(r'^$', 'structure.views.welcome'),
)
