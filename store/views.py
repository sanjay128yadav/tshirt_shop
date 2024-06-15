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

API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/');


# Create your views here.

def home(request):

    tshirts = []

    tshirts = Tshirt.objects.all()

    query = request.GET

    brand    = query.get('brand')
    idealFor = query.get('idealFor')
    occasion = query.get('occasion')
    neckType = query.get('neckType')
    sleeve   = query.get('sleeve')
    color    = query.get('color')

    if brand !="" and brand is not None:
       tshirts = tshirts.filter(brand__slug = brand)
    if neckType !="" and neckType is not None:
       tshirts = tshirts.filter(neck_type__slug = neckType) 
    if occasion !="" and occasion is not None:
       tshirts = tshirts.filter(Occasion__slug = occasion) 
    if idealFor !="" and idealFor is not None:
       tshirts = tshirts.filter(ideal_for__slug = idealFor) 
    if sleeve !="" and sleeve is not None:
       tshirts = tshirts.filter(Sleeve__slug = sleeve) 
    if color !="" and color is not None:
       tshirts = tshirts.filter(color__slug = color)     

    occasions = Occasion.objects.all()
    brands = Brand.objects.all()
    neckTypes = NeckType.objects.all()
    sleeves = Sleeve.objects.all()
    colors = Color.objects.all()
    idealFors = IdealFor.objects.all()    

    #tshirts = Tshirt.objects.filter(brand__slug = brand)
    cart = request.session.get('cart')
    print(cart)
    """
    for t in tshirts:
        #all_sizes = t.sizevariant_set.all()
        min_price = t.sizevariant_set.all().order_by('price').first()
        #print(t , min_price.price, min_price.size)
        t.min_price = min_price.price
        t.after_discount = t.min_price - (t.min_price * t.discount /100)
        t.after_discount = floor(t.after_discount)
    """
    context = {
        "tshirts" : tshirts,
        "occasions" : occasions,
        "brands" : brands,
        "neckTypes" : neckTypes,
        "sleeves" : sleeves,
        "colors" : colors,
        "idealFors" : idealFors
    }
    return render(request , template_name='store/home.html' , context = context)

def cart(request):
    cart = request.session.get('cart')
    if cart is None:
        cart = []

    for c in cart:
        tshirt_id = c.get('tshirt')
        tshirt = Tshirt.objects.get(id=tshirt_id) 
        c['tshirt']  =  tshirt 
        c['size'] = SizeVariant.objects.get(tshirt_id = tshirt, size = c['size'])
    #print(cart)    
    return render(request , template_name='store/cart.html', context= {'cart':cart})

@login_required(login_url = '/login/')    
def orders(request):
    user = request.user
    print(user)
    orders = Order.objects.filter(user = user).order_by('-date').exclude(order_status = 'PENDING')
    context = {
        'orders' : orders 
    }
    return render(request , template_name='store/orders.html', context = context)
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
            user = form.save();
            user.email = user.username
            user.save()
            print(user)
            return render(request , template_name='store/login.html')
        else:
            context = {
                "form": form
            }
            return render(request , template_name='store/signup.html' , context= context)


def signout(request):
    #request.session.clear()
    logout(request)
    return render(request , template_name='store/home.html')

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

def add_to_cart(request, slug, size):
    user = None    
    if request.user.is_authenticated:
       user = request.user 
    cart = request.session.get('cart')
    if cart is None:
        cart = []

    tshirt = Tshirt.objects.get(slug = slug)
    add_cart_for_anom_user(cart, size, tshirt) 

    if user is not None:        
        add_cart_to_database(user, size, tshirt)
        
    request.session['cart'] = cart
    return_url = request.GET.get('return_url')
    return redirect(return_url)

def add_cart_to_database(user , size, tshirt):
    size_temp =  SizeVariant.objects.get(size = size , tshirt = tshirt)
    existing =  Cart.objects.filter( user = user , sizeVariant = size_temp)
    if len(existing) >0:
        obj = existing[0]   
        obj.quantity =  obj.quantity +1
        obj.save() 
    else:
        c = Cart()
        c.user = user
        c.sizeVariant = size_temp
        c.quantity = 1
        c.save()

def add_cart_for_anom_user(cart , size, tshirt):
    flag = True 
    cart_obj = None  # Define cart_obj outside the loop
    for cart_obj in cart:
        t_id = cart_obj.get('tshirt')  # Corrected 'thsirt' to 'tshirt'
        size_short = cart_obj.get('size')
        if t_id == tshirt.id and size_short == size:
            flag = False
            cart_obj['quantity'] = cart_obj['quantity'] + 1
    if flag:
        cart_obj = {
            'tshirt': tshirt.id,
            'size': size,
            'quantity': 1
        }
        cart.append(cart_obj)

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
         



