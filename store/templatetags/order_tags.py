from django import template
from math import floor

register = template.Library()

@register.filter
#@register.order_tag

@register.simple_tag
def get_order_status_class(status): 
    if status == 'COMPLETED':
        return 'success'
    else:
        return 'warning'
                           


