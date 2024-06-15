from django.shortcuts import render , HttpResponse , redirect
from store.forms.authforms import CustomerCreationForm , CustomerAuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Tshirt, SizeVariant , Cart, Order, OrderItem, Payment, Occasion, IdealFor, NeckType
from store.models import Sleeve, Brand, Color
from math import floor
from django.contrib.auth.decorators import login_required
from store.forms.checkout_form import CheckoutForm

@login_required(login_url = '/login/')    
def orders(request):
    user = request.user
    print(user)
    orders = Order.objects.filter(user = user).order_by('-date').exclude(order_status = 'PENDING')
    context = {
        'orders' : orders 
    }
    return render(request , template_name='store/orders.html', context = context)