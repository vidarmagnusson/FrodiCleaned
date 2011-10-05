from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('schools.views',
	url(r'^$', 'schools.list_feeds'),

	url(r'^leikskolar/$', 'schools.list_feeds', kwargs={'level':'preschool'}),
	url(r'^leikskolar/skolar/allir-skolar/$', 'schools.list_schools', kwargs={'level':'preschool'}),
	url(r'^leikskolar/skolar/landssvaedi/(?P<area>[^/]*)/$', 'schools.list_schools', kwargs={'level':'preschool'}),

	url(r'^grunnskolar/$', 'schools.list_feeds', kwargs={'level':'primary'}),
	url(r'^grunnskolar/skolar/allir-skolar/$', 'schools.list_schools', kwargs={'level':'primary'}),
	url(r'^grunnskolar/skolar/landssvaedi/(?P<area>[^/]*)/$', 'schools.list_schools', kwargs={'level':'primary'}),

	url(r'^framhaldsskolar/$', 'schools.list_feeds', kwargs={'level':'secondary'}),
        url(r'^framhaldsskolar/skolar/allir-skolar/$', 'schools.list_schools', kwargs={'level':'secondary'}),
	url(r'^framhaldsskolar/skolar/landssvaedi/(?P<area>[^/]*)/$', 'schools.list_schools', kwargs={'level':'secondary'}),

	url(r'^skoli/(?P<school>[^/]*)/$', 'schools.school_info', name='school-info'),
)

urlpatterns += patterns('country.views',
        url(r'^leikskolar/skolar/landssvaedi/$', 'regions.list_areas', kwargs={'color':settings.PRESCHOOL_COLOR}),
        url(r'^grunnskolar/skolar/landssvaedi/$', 'regions.list_areas', kwargs={'color':settings.PRIMARY_SCHOOL_COLOR}),
        url(r'^framhaldsskolar/skolar/landssvaedi/$', 'regions.list_areas', kwargs={'color':settings.SECONDARY_SCHOOL_COLOR}),
)
