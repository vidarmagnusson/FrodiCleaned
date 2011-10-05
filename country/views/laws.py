from country.models.laws import Law
from structure.shortcuts import render

"""
A view method which fetches a specific law, given by a number parameter (the
number of the law). If no number is provided the view gets the first law object
of the site. The graceful error handling of this method must be changed, it is
too random at the moment
"""
def view_law(request, number=None):
	# Try to get the law based on the number (or just return the first
	# law of this site
	try:
		if number:
			law = Law.objects.get(number=number)
		else:
			law = Law.on_site.all()[1]
	except:
		return render('country/law.html', {}, request)

	# Return the law and the sections (might need to redo this rendering)
	return render('country/law.html', {'title':law.title, 'sections':law.section_set.all()}, request)

