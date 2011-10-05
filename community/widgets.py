#! -*- encoding: utf-8 -*-
from django.forms import HiddenInput, MultipleHiddenInput
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

from schools.models.schools import School

class SelectStartDate(HiddenInput):
	def render(self, name, value, attrs):
		ret = super(SelectStartDate, self).render(name, value, attrs)
		ret += u'<div>Byrjar: <input style="width:90px; margin:5px;" type=text id="%s_day" maxlength="10"> klukkan <input type="text" id="%s_time" style="width:60px" maxlength="5"></div>' % (name, name)
		return ret

	class Media:
		js = ('/media/js/from-to-date-picker.js',)

# This should be the same widget as SelectStartDate
class SelectEndDate(HiddenInput):
	def render(self, name, value, attrs):
		ret = super(SelectEndDate, self).render(name, value, attrs)
		ret += u'<div>Klárast: <input style="width:90px; margin:5px;" type=text id="%s_day" maxlength="10"> klukkan <input style="width:60px;"type="text" id="%s_time" maxlength="5"></div>' % (name, name)
		return ret

	class Media:
		js = ('/media/js/from-to-date-picker.js',)

class SchoolSelection(MultipleHiddenInput):
	def render(self, name, value, attrs):
		ret = '<input id="input_school" class="bucket" name="school">'
		ret += '<ul id="school_list" class="hide-on-load">'
		for school in School.objects.all():
			ret += '<li id="school_%s"><a id="%s" href="#" class="raindrop">%s</a></li>' % (school.id, school.name, school.name)
		ret += '</ul>'
		return mark_safe(ret)
