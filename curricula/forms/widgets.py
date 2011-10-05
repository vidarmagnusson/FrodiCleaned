#! -*- encoding: utf-8 -*-
from django.forms import TextInput, HiddenInput, MultipleHiddenInput, SelectMultiple
from django.forms.widgets import RadioFieldRenderer
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

from curricula.models.courses import Goal

class RenderLevels(RadioFieldRenderer):
	def render(self):
		return mark_safe(u' '.join([u'%s' % force_unicode(w) for w in self]))

class SliderInput(TextInput):
	def render(self, name, value, attrs):
		res = super(SliderInput, self).render(name, value, attrs=attrs)
		res += '<div class="slider-wrapper">'
		res += '<div id="%s_slider" class="slider"></div>' % name
		res += '<div id="%s_slider_value" class="slider-value">%s</div>' % (name, value)
		res += '<div id="%s_slider_unit" class="slider-unit"></div>' % name
		res += '</div>'
		return mark_safe(res)
            
	class Media:
		js = ('/media/js/slider.js',)

class AddGoalInput(MultipleHiddenInput):
	def render(self, name, value, attrs):
		attributes = attrs
		previous_values = ''
		if value:
			for pk in value:
				try:
					previous_values += u'<li id="%s_item%s" class="goal-item">%s</li>' % (name,pk, Goal.objects.get(pk=int(pk)))
				except:
					pass
		
		if name.count('knowledge_goals'):
			question = u'Nemandi skal hafa öðlast þekkingu og skilning til að:'
		elif name.count('skills_goals'):
			question = u'Nemandi skal hafa öðlast leikni í að:'
		elif name.count('competence_goals'):
			question = u'Nemandi skal geta hagnýtt þá almennu þekkingu og leikni sem hann hefur aflað sér til að:'

		res = u'<div id="%s_wrapper">' % name
		res += super(AddGoalInput, self).render(name, value, attrs=attributes)
		res += u'</div>'
		res += u'<div class="add-wrapper">'
		if question:
			res += u'<div class="prepend_question">%s</div>' % question
		res += u'<ul id="%s_added" class="added">%s</ul>' % (name, previous_values)
		res += u'<button id="%s_add" class="add-to-list button">Bæta við viðmiði</button><br/>' % name
		res += u'</div>'

		return mark_safe(res)

	class Media:
		js = ('/media/js/add-new-dialog.js',)

"""
Widget for adding a list of user profiles (with images and names).
Combined with the javascript defined in the Media class it allows 
a more graphic selection of authors (people) from a list.

Choices must be defined and the the method assumes that the current
user is the first choice from that list. If choices list is empty
this widget will fail.
"""
class MultipleAuthorInput(MultipleHiddenInput):
	def render(self, name, value, attrs):
		# Authors are kept in choices
		authors = self.choices

		# Wrapper div
		res = u'<div id="%s_wrapper" class="author-list">' % name
		res += super(MultipleAuthorInput, self).render(name, value, attrs=attrs)

		# Rest of authors
		res += '<ul id="possible-authors">'

		# If authors are found add a small description
		# If not explain that you are a lonely user
		if authors:
			res += u'<li>Veldu meðhöfunda úr listanum hér fyrir neðan ef þú vilt</li>'
		else:
			res += u'<li>Þú ert ekki áskrifandi að neinum notanda og getur því ekki bætt neinum við sem meðhöfundi.</li>'

		# Add all the other authors to the list and make the "not-selected"
		# In future this will need to change when older values are used to fill in
		for friend in authors:
			res += u'<li id="coauthor_%s" class="author-item not-selected">' % friend.user_id
			res += u'<img src="%s" alt="%s"> %s' % (friend.avatar, friend.title, friend.title)
			res += u'</li>'
		res += '</ul>'

		# Create div container for hidden inputs
		res += u'<div id="add-author"></div>'
		res += u'</div>'

		# Return the html rendering of the widget
		return mark_safe(res)

	class Media:
		js = ('/media/js/add-authors.js',)

class ProfessionInput(MultipleHiddenInput):
	def render(self, name, value, attrs):
		res = '<div id="%s-wrapper">' % name
		res += super(ProfessionInput, self).render(name, value, attrs=attrs)
		res += '<input type="text" id="%s-input" class="input-filter" name="%s-input">' % (name, name)
		res += '</div>'
		return mark_safe(res)

class CourseSelection(MultipleHiddenInput):
	def render(self, name, value, attrs):
		res = '<div id="%s-wrapper" class="package-selector">' % name[2:]
		res += '<div class="new-package"></div>'
		res += '<div class="package-list"></div>'
		res += '</div>'

		return mark_safe(res)
