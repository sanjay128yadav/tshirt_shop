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
    
@register.simple_tag
def multiply(a , b):    
    return a*b  

@register.simple_tag
def calc_sale_price(price , discount):    
    salePrice = floor(price - (price * (discount / 100) ))
    return salePrice  

@register.filter
def calc_total_payble_amount(cart):    
    total = 0
    for c in cart:
        price       = c.get('size').price
        discount    = c.get('tshirt').discount
        sale_price = calc_sale_price(price, discount)
        total_of_single_product = sale_price * c.get('quantity')
        total = total + total_of_single_product
    return total

