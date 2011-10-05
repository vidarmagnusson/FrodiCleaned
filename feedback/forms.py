from django.forms import ModelForm
from feedback.models import *

class FeedbackForm(ModelForm):
	class Meta:
		model = Feedback

class CommentForm(ModelForm):
	class Meta:
		model = Comment
