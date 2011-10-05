from django.template import Library
register = Library()
from django.template.defaultfilters import stringfilter

@register.filter(name='truncatestring')
@stringfilter
def truncatestring(src, ln):
    ret = src[:ln]
    if len(src)>ln:
        ret = ret[:ln-3]+'...'
    return ret

