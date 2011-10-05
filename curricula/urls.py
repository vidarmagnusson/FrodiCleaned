# Curriculum - Web application for creating and managing educational curricula
# Copyright (C) 2010  The Ministry of Education, Science and Culture, Iceland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import *
from curricula.forms.programmes import ProgrammeCreateForm, ProgrammeDescriptionForm, ProgrammeOrganizationForm, ProgrammeCompetenceForm, ProgrammeEvaluationForm, ProgrammeCoursesForm, ProgrammeWizard
from curricula.forms.courses import CourseCreateForm, CourseDescriptionForm, CourseGoalForm, CourseEvaluationAuthorForm, CourseWizard


urlpatterns = patterns('curricula',
#	(r'^$', 'html.index'),        
	url(r'^framhaldsskolar/afangar/minir-afangar/$', 'views.my_courses', name='my-courses'),
	url(r'^framhaldsskolar/afangar/osamthykktir-afangar/$', 'views.unapproved_courses', name='unapproved_courses'),
        url(r'^framhaldsskolar/afangar/fyrirmyndarafangar/$', 'views.list_exemplary_courses', name='list-exemplary-courses'),
	url(r'^framhaldsskolar/afangar/fyrirmyndarafangar/fyrirmyndarafangi/(?P<id>[^/]*)/$', 'views.view_exemplary_course', name='view-exemplary-course'),

	url(r'^framhaldsskolar/afangar/afangi/(?P<id>[^/]*)/$', 'views.view_course', name='view-course'),
	url(r'^framhaldsskolar/afangar/birta/(?P<id>[^/]*)/$', 'views.publish_course', name='publish-course'),
	url(r'^framhaldsskolar/afangar/eyda/(?P<id>[^/]*)/$', 'views.delete_course', name='delete-course'),
	url(r'^framhaldsskolar/afangar/samthykkja/(?P<id>[^/]*)/$', 'views.approve_course', name='approve-course'),
	url(r'^framhaldsskolar/afangar/endurvekja/(?P<id>[^/]*)/$', 'views.reactivate_course', name='reactivate-course'),

	url(r'^framhaldsskolar/afangar/nyr-afangi/$', CourseWizard([CourseCreateForm, CourseDescriptionForm, CourseGoalForm, CourseEvaluationAuthorForm])),
	url(r'^framhaldsskolar/brautir/ny-braut/$', ProgrammeWizard([ProgrammeCreateForm, ProgrammeDescriptionForm, ProgrammeOrganizationForm, ProgrammeCompetenceForm, ProgrammeEvaluationForm, ProgrammeCoursesForm])),

        url(r'^raduneytisstjornbord/stillingar-fyrir-framhaldsskola/namslokategundir/', 'views.list_professions'),
        url(r'^raduneytisstjornbord/stillingar-fyrir-framhaldsskola/proflokategundir/', 'views.list_exams'),
        url(r'^raduneytisstjornbord/stillingar-fyrir-framhaldsskola/namssvid/', 'views.list_fields'),
        url(r'^raduneytisstjornbord/stillingar-fyrir-framhaldsskola/fyrirmyndarafangar/$', 'views.list_exemplary_courses', name='adminlist-exemplary-courses'),
        url(r'^raduneytisstjornbord/stillingar-fyrir-framhaldsskola/fyrirmyndarafangar/nyr-fyrirmyndarafangi/(?P<id>[^/]*)/$', 'views.make_exemplary_course', name='make-exemplary-course'),
	
)
