from django.shortcuts import render , HttpResponse , redirect
#from django.contrib.auth.forms import UserCreationForm
from store.forms.authforms import CustomerCreationForm , CustomerAuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Tshirt
from math import floor


# Create your views here.

def home(request):
    tshirts = Tshirt.objects.all()
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
    return render(request , template_name='store/cart.html')
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

def show_prduct(request , id):
    tshirt = Tshirt.objects.get(pk=id)
    
    if request.GET.get('size'):
        sizeget = request.GET.get('size')
    else:
        sizeget = 'S'

    sizeobj = tshirt.sizevariant_set.get(size = sizeget)
    size_price = sizeobj.price
    sale_price = size_price - (size_price * (tshirt.discount / 100))    
    context = {
        'tshirt': tshirt , 'price': size_price , 'sale_price': sale_price
    }
    return render(request, template_name='store/product_detail.html', context= context)

