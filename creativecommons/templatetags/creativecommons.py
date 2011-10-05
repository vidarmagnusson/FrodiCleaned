from django.template import Library
register = Library()

"""
A template tag which converts a alphanumerical number to a roman numerical 
(used to represent chapters in laws (at least in Iceland). If the src parameter
is not an integer or a long the 'src' is return as is. It is possible to pass
in to the method arguments. The only one supported at the moment is 'lowercase'
which renders the roman numerical in lowercase.
"""
@register.filter(name='mark_small')
def mark_small(license, author):
	return license.html_mark_small(author)

