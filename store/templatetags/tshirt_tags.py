from django import template
from math import floor

register = template.Library()

@register.filter

def rupee(number):
    return f'(₹) {number}'

@register.simple_tag

#def get_website_name():
#    return "simple.com"

def min_price(tshirt):
    size = tshirt.sizevariant_set.all().order_by('price').first()
    return floor(size.price)

@register.simple_tag
def sale_price(tshirt):
    price = min_price(tshirt)
    discount = tshirt.discount
    salePrice = floor(price - (price * (discount / 100) ))
    return salePrice

@register.simple_tag
def get_active_size_button_class(active_size, size):
    if active_size.size == size.size:
        return "dark"
    else:
        return "light"

