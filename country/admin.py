from country.models.regions import Municipality, CountryArea
from country.models.laws import Article, Section, Law
from django.contrib import admin

admin.site.register(Municipality)
admin.site.register(CountryArea)

admin.site.register(Article)
admin.site.register(Section)
admin.site.register(Law)
