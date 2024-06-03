from django.shortcuts import render , HttpResponse , redirect
#from django.contrib.auth.forms import UserCreationForm
from store.forms.authforms import CustomerCreationForm , CustomerAuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Tshirt, SizeVariant
from math import floor


# Create your views here.

def home(request):
    tshirts = Tshirt.objects.all()
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
        "tshirts" : tshirts
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
def orders(request):
    return render(request , template_name='store/orders.html')
def login(request):
    if request.method == 'GET':
        form = CustomerAuthForm
        return render(request , template_name='store/login.html', context= { 'form' : form })
    else:
        #print(request.POST)
        form = CustomerAuthForm(data = request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user:
                loginUser(request , user)
                return redirect('homepage')
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
    #print(slug , size)   

    cart = request.session.get('cart')
    if cart is None:
        cart = []

    tshirt = Tshirt.objects.get(slug = slug)
    flag = True
    cart_obj = None  # Define cart_obj outside the loop
    for cart_obj in cart:
        t_id = cart_obj.get('tshirt')  # Corrected 'thsirt' to 'tshirt'
        size_temp = cart_obj.get('size')
        if t_id == tshirt.id and size_temp == size:
            flag = False
            cart_obj['quantity'] = cart_obj['quantity'] + 1

    if flag:
        cart_obj = {
            'tshirt': tshirt.id,
            'size': size,
            'quantity': 1
        }
        cart.append(cart_obj) 
    request.session['cart'] = cart
    return_url = request.GET.get('return_url')
    return redirect(return_url)

