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

def validatePayment(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    payment_request_id = request.GET.get('payment_request_id')
    payment_id = request.GET.get('payment_id')  
    # Create a new Payment Request
    response = API.payment_request_payment_status(payment_request_id, payment_id)
    # status = response['payment_request']['payment']['status']
    status = response.get('payment_request').get('payment').get('status')
    print(status)   # Payment status  
    
    if status != "Failed":
        print("Payment Success")
        try:
            payment = Payment.objects.get(payment_request_id = payment_request_id)
            payment.payment_id = payment_id
            payment.payment_status = status
            payment.save()

            order = payment.order
            order.order_status = "Placed"
            order.save()

            cart = []
            request.session['cart'] = cart
            Cart.objects.filter(user = user).delete()
            return redirect('/orders/')  
        except:
            return render(request , template_name='store/payment_failed.html')
    else:
        return render(request , template_name='store/payment_failed.html')