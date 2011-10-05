from schools.models.schools import *
from schools.models.housing import *
from schools.models.students import *
from schools.models.registration import *

from django.contrib import admin

admin.site.register(School)
admin.site.register(Preschool)
admin.site.register(PrimarySchool)
admin.site.register(SecondarySchool)
admin.site.register(University)
admin.site.register(LearningCenter)
admin.site.register(SchoolInformation)

admin.site.register(Housing)
admin.site.register(RoomType)
admin.site.register(Service)
admin.site.register(ServiceOffering)

admin.site.register(StudentSociety)

admin.site.register(RegistrationInformation)
