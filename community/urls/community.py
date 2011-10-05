from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('community.views',
	url(r'^$', 'various.index'),
	url(r'^efni/(?P<entry>[^/]*)/$', 'various.show_entry', name='view-entry'),
	url(r'^efni/sia-ut/(?P<construct>[^/]*)/$', 'various.index', name='filter-timeline'),
	url(r'^notandi/(?P<username>[^/]*)/$', 'various.index', name='user-timeline'),
	url(r'^notandi/(?P<username>[^/]*)/vinir/$', 'various.friends', name='friends-timeline'),
	url(r'^notandi/(?P<username>[^/]*)/sia-ut/(?P<construct>[^/]*)/$', 'various.index', name='filter-user-timeline'),


        url(r'^flokkar/(?P<tag>[^/]*)/$', 'social.tags', name='view-tag-info'),
        url(r'^skilabod/$', 'various.list_private_messages', name='list-private-messages'),
        url(r'^hopar/nyr$', 'various.create_group', name='create-group'),
        url(r'^hopar/$', 'various.list_groups', name='group-list'),
        url(r'^hopur/taka-thatt/$', 'various.join_group', name='join-group'),
        url(r'^hopur/fara/$', 'various.leave_group', name='leave-group'),
        url(r'^hopur/(?P<group_id>[^/]*)/$', 'various.group', name='group-info'),
        url(r'^skilabod/innholf$', 'various.list_private_messages', kwargs={'postbox':'inbox'}, name='list-private-messages'),
        url(r'^skilabod/utholf$', 'various.list_private_messages', kwargs={'postbox':'outbox'}, name='list-private-messages'),

        url(r'^minar-stillingar/$', 'various.my_person', name='personal-profile'),

        url(r'^innsending/$', 'various.new', name='new-activity'),
	url(r'^vidburdur/nyr/$', 'events.new', name='new-event'),

	url(r'^ahugavert/$', 'various.mark_like', name='mark-like'),
	url(r'^ovideigandi/$', 'various.index', name='flag'),
	url(r'^deila/$', 'various.share', name='share'),
	url(r'^fylgja/$', 'various.follow', name='start-following')

)

