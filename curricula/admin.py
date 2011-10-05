from curricula.models.fields_and_exams import *
from curricula.models.courses import *
from curricula.models.programmes import *
from curricula.models.extra_information import *
from django.contrib import admin

admin.site.register(Subject)
admin.site.register(SubjectCombination)
admin.site.register(Topic)
admin.site.register(TopicCombination)
admin.site.register(Goal)
admin.site.register(Evaluation)
admin.site.register(Course)
admin.site.register(ExemplaryCourse)

admin.site.register(ExamLevel)
admin.site.register(Exam)
admin.site.register(ExtraRule)
admin.site.register(SubjectLevel)
admin.site.register(Field)
admin.site.register(SubField)
admin.site.register(Profession)
admin.site.register(CoursePackage)
admin.site.register(KeyCompetence)
admin.site.register(KeyCompetenceGoal)
admin.site.register(Programme)

admin.site.register(Stakeholder)
admin.site.register(SchoolCurriculum)
admin.site.register(CurriculumAdministrator)
