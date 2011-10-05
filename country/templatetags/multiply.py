from django.template import Library
register = Library()

"""
A simple template tag used to multiply two numbers together
"""
@register.filter(name='multiply')
def multiply(value, arg):
    return int(value) * int(arg) 


