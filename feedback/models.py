from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
	title = models.CharField('titill', max_length=128)
	description = models.TextField('hugmynd')
	author = models.ForeignKey(User, editable=False)
	published = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
	feedback = models.ForeignKey(Feedback, editable=False)
	comment = models.TextField('athugasemd')
	author = models.ForeignKey(User, editable=False, related_name='feedback_comment')
	published = models.DateTimeField(auto_now_add=True)

