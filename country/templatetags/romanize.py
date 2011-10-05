from django.template import Library
register = Library()

from roman import toRoman

"""
A template tag which converts a alphanumerical number to a roman numerical 
(used to represent chapters in laws (at least in Iceland). If the src parameter
is not an integer or a long the 'src' is return as is. It is possible to pass
in to the method arguments. The only one supported at the moment is 'lowercase'
which renders the roman numerical in lowercase.
"""
@register.filter(name='romanize')
def romanize(src, args=None):
	# Check if instance is int or long
	if isinstance(src, int) or isinstance(src, long):
		if args != None:
			# If args is 'lowercase' return lowercased roman numerical
			if args.lower() == 'lowercase':
				return toRoman(src).lower()

		# Return the roman numerical equivalent
		return toRoman(src)
	else:
		# src wasn't int or long so we just return it
		return src

