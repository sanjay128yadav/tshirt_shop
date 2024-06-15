from django.shortcuts import render , HttpResponse , redirect
from store.forms.authforms import CustomerCreationForm , CustomerAuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Tshirt, SizeVariant , Cart, Order, OrderItem, Payment, Occasion, IdealFor, NeckType
from store.models import Sleeve, Brand, Color
from math import floor
from django.contrib.auth.decorators import login_required
from store.forms.checkout_form import CheckoutForm

def show_prduct(request , slug):
    tshirt = Tshirt.objects.get(slug=slug)    
    
    if request.GET.get('size'):
        sizeget = request.GET.get('size')
    else:        
        sizeget = tshirt.sizevariant_set.all().order_by('price').first().size

    sizeobj = tshirt.sizevariant_set.get(size = sizeget)
    size_price = sizeobj.price
    sale_price = size_price - (size_price * (tshirt.discount / 100))    
    context = {
        'tshirt': tshirt , 'price': size_price , 'sale_price': sale_price, 'active_size': sizeobj
    }
    return render(request, template_name='store/product_detail.html', context= context)