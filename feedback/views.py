from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from feedback.models import Feedback
from feedback.forms import FeedbackForm, CommentForm
from structure.shortcuts import render

@login_required
def list_feedbacks(request):
	if request.method == 'POST':
		form = FeedbackForm(request.POST)
		if form.is_valid():
			feedback = form.save(commit=False)
			feedback.author = request.user
			feedback.save()

	feedbacks = Feedback.objects.all().order_by('-published')
	feedback_list = []
	for feedback in feedbacks:
		feedback_list.append({'feedback':feedback, 'commentform': CommentForm(initial={'feedback':feedback})})

	new_feedback = FeedbackForm()

	return render('feedback/feedback_list.html', {'feedback':feedback_list, 'form':new_feedback}, request)

@login_required
def comment_on_feedback(request, feedback):
	print feedback
	if request.method == 'POST':
		try:
			form = CommentForm(request.POST)
			feedback = Feedback.objects.get(pk=int(feedback))
			if form.is_valid():
				comment = form.save(commit=False)
				comment.author = request.user
				comment.feedback = feedback
				comment.save()
		except:
			pass

	return HttpResponseRedirect(reverse('feedback-list'))
