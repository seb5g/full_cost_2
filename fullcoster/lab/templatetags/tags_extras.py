from django import template
#from full_cost.version import get_version


register = template.Library()

@register.filter
def get_at_index(list, index):
    return list[index]

@register.filter
def get_index_from_value(list, val):
    return list.index(val)

#@register.simple_tag
#def get_version():
#    return get_version()