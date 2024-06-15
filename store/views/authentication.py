from django.shortcuts import render , HttpResponse , redirect
#from django.contrib.auth.forms import UserCreationForm
from store.forms.authforms import CustomerCreationForm , CustomerAuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Tshirt, SizeVariant , Cart, Order, OrderItem, Payment, Occasion, IdealFor, NeckType
from store.models import Sleeve, Brand, Color
from math import floor
from django.contrib.auth.decorators import login_required
# from store.forms.checkout_form import CheckoutForm
from store.forms import CheckoutForm, CustomerCreationForm, CustomerAuthForm

def login(request):
    if request.method == 'GET':
        form = CustomerAuthForm
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page
        return render(request , template_name='store/login.html', context= { 'form' : form })
    else:
        print(request.POST)
        form = CustomerAuthForm(data = request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user:
                loginUser(request , user)

                session_cart = request.session.get('cart')
                if session_cart is None:
                    session_cart = []
                else:
                    for c in session_cart:
                        size = c.get('size')
                        tshirt_id = c.get('tshirt')    
                        quantity = c.get('quantity')    
                        cart_obj = Cart()
                        cart_obj.sizeVariant = SizeVariant.objects.get(size = size , tshirt = tshirt_id)
                        cart_obj.quantity = quantity
                        cart_obj.user = user
                        cart_obj.save()

                cart = Cart.objects.filter(user = user)
                session_cart = []
                for c in cart:
                    obj = {
                        'size' : c.sizeVariant.size,
                        'tshirt' : c.sizeVariant.tshirt.id,
                        'quantity' : c.quantity 
                    }
                    session_cart.append(obj)  
                request.session['cart'] =  session_cart 
                next_page = request.session.get('next_page')
                if next_page is None:
                    next_page = 'homepage'
                return redirect(next_page)
        else:
            #form = AuthenticationForm
            return render(request , template_name='store/login.html', context= { 'form' : form })

def signup(request):

    if (request.method == 'GET'):
        form = CustomerCreationForm()
        context = {
            "form": form
        }
        return render(request , template_name='store/signup.html' , context= context)
    else:
        form = CustomerCreationForm(request.POST)
        #print(form.is_valid())
        #print(form.errors)
        #return HttpResponse("Signup")

        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()            
            return redirect('login')
            # return render(request , template_name='store/login.html')
        else:
            context = {
                "form": form
            }
            return render(request , template_name='store/signup.html' , context= context)

def signout(request):
    #request.session.clear()
    logout(request)
    return render(request , template_name='store/home.html')                