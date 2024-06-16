from django.shortcuts import render , HttpResponse , redirect
from store.forms.authforms import CustomerCreationForm , CustomerAuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Tshirt, SizeVariant , Cart, Order, OrderItem, Payment, Occasion, IdealFor, NeckType
from store.models import Sleeve, Brand, Color
from math import floor
from django.contrib.auth.decorators import login_required
from store.forms.checkout_form import CheckoutForm
from django.views.generic.detail import DetailView

class ProductDetailView(DetailView):
    template_name = 'store/product_detail.html'
    model = Tshirt
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tshirt = context.get('tshirt')
        request = self.request  
    
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
        return context
