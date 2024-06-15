from django.shortcuts import render , HttpResponse , redirect
#from django.contrib.auth.forms import UserCreationForm
from store.forms.authforms import CustomerCreationForm , CustomerAuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Tshirt, SizeVariant , Cart, Order, OrderItem, Payment, Occasion, IdealFor, NeckType
from store.models import Sleeve, Brand, Color
from math import floor
from django.contrib.auth.decorators import login_required
from store.forms.checkout_form import CheckoutForm

from django.http import HttpResponse
from instamojo_wrapper import Instamojo
from Tshop.settings import API_KEY , AUTH_TOKEN

API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

@login_required(login_url = '/login/')
def checkout(request):
    # Handle GET request
    if request.method == 'GET':
        form = CheckoutForm()
        cart = request.session.get('cart')
        if cart is None:
            cart = []

        for c in cart:
            size_str = c.get('size')
            tshirt_id = c.get('tshirt')
            size_obj  = SizeVariant.objects.get(size = size_str , tshirt = tshirt_id)   
            c['size'] = size_obj
            c['tshirt'] =  size_obj.tshirt  
            
        return render(request , template_name='store/checkout.html' , context= { 'form' : form , 'cart': cart })
    else:
        # Handle POST request        
        form = CheckoutForm(request.POST)
        user = None
        if request.user.is_authenticated:
            user = request.user
        if form.is_valid():
            # Pament
            cart = request.session.get('cart')
            if cart is None:
                cart = []

            for c in cart:
                size_str = c.get('size')
                tshirt_id = c.get('tshirt')
                size_obj  = SizeVariant.objects.get(size = size_str , tshirt = tshirt_id)   
                c['size'] = size_obj
                c['tshirt'] =  size_obj.tshirt  

            shipping_address = form.cleaned_data.get('shipping_address')
            phone = form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method') 
            total = calc_total_payble_amount(cart)
            print(shipping_address , phone, payment_method, total)

            order = Order()
            order.shipping_address = shipping_address
            order.phone = phone
            order.payment_method = payment_method
            order.total = total
            order.order_status = "PENDING"
            order.user = user
            order.save()

            # for saving order items
            for c in cart:
                order_item = OrderItem()
                order_item.order = order
                size = c.get('size')
                tshirt = c.get('tshirt')
                order_item.price =  floor( size.price - (size.price * (tshirt.discount / 100) ))
                order_item.quantity = c.get('quantity')
                order_item.size = size
                order_item.tshirt = tshirt
                order_item.save()

            # Creating Payment            
            response = API.payment_request_create(
                amount=order.total,
                purpose='Payment for Tshirts',
                send_email=False,
                buyer_name= f'{ user.first_name} {user.last_name}',
                email=user.email,
                redirect_url="http://localhost:8000/validate_payment"
                ) 
            print(user.first_name, user.last_name, user.email,'WIP', user)
            payment_request_id = response['payment_request']['id'] 
            url = response['payment_request']['longurl'] 

            payment = Payment()
            payment.order = order 
            payment.payment_request_id = payment_request_id
            payment.save()            
            #return HttpResponse("Checkout successful")
            return redirect(url)
        else:
            return redirect('/checkout/')
        
#utility function
def calc_total_payble_amount(cart):    
    total = 0
    for c in cart:        
        discount = c.get('tshirt').discount
        price = c.get('size').price        
        sale_price = floor(price - (price * (discount / 100) ))
        total_of_single_product = sale_price * c.get('quantity')
        total = total + total_of_single_product
    return total         