from django.template import Library
register = Library()

@register.filter(name='objecttype')
def objecttype(activityconstruct):
	return activityconstruct.ostatus()['objecttype']
