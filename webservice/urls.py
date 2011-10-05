from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('webservice.views',
	(r'^country/map/mark/(?P<area>[^/]*)/$', 'country.mark'),

        url(r'^namskra/framhaldsskolar/abbreviations/$', 'curricula.abbreviations', name='webservice-abbreviations'),
        url(r'^namskra/framhaldsskolar/topics/cloud/$', 'curricula.topic_cloud', name='webservice-topic-cloud'),
        url(r'^namskra/framhaldsskolar/goal/new/$', 'curricula.create_goal', name='webservice-new-goal'),
        url(r'^namskra/framhaldsskolar/goal/delete/$', 'curricula.delete_goal', name='webservice-delete-goal'),

        url(r'^namskra/framhaldsskolar/professions/$', 'curricula.get_professions', name='webservice-professions'),
        url(r'^namskra/framhaldsskolar/competence/new/$', 'curricula.create_key_competence_goal', name='webservice-new-competence'),
        url(r'^namskra/framhaldsskolar/competence/delete/$', 'curricula.delete_key_competence_goal', name='webservice-delete-competence'),
        url(r'^namskra/framhaldsskolar/competence/get/$', 'curricula.get_key_competence_id', name='webservice-get-competence'),

	url(r'^samfelag/tag/$', 'community.tag', name='webservice-community-tag'),
	url(r'^samfelag/comment/$', 'community.comment', name='webservice-community-comment'),
	url(r'^samfelag/location/$', 'community.location', name='webservice-community-location'),

)
