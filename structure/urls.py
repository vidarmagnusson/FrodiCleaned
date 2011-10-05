from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url('^efnislausar-sidur/$', 'structure.views.list_empty'),
	url('^nytt-efni(?P<url>/.*)', 'structure.views.create_flatpage', name='modify-page'),
	url('^hlidarreitir/$', 'structure.views.create_highlight'),
)
