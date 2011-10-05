from django.forms import ModelForm, Form
from django.shortcuts import render_to_response
from django.contrib.formtools.wizard import FormWizard
from django.http import HttpResponseRedirect

from curricula.models.extra_information import Stakeholder

"""
Stakeholder form to create a new stakeholder (or update it)
"""
class StakeholderForm(ModelForm):
	class Meta:
		model = Stakeholder
