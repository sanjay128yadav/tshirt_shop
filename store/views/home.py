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
from django.core.paginator import Paginator
from urllib.parse import urlencode

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
    page     = query.get('page')

    if (page is None or page == ''):
       page = 1

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
    if color !="" and brand is not None:
       tshirts = tshirts.filter(color__slug = color)     

    occasions = Occasion.objects.all()
    brands = Brand.objects.all()
    neckTypes = NeckType.objects.all()
    sleeves = Sleeve.objects.all()
    colors = Color.objects.all()
    idealFors = IdealFor.objects.all()    

    #tshirts = Tshirt.objects.filter(brand__slug = brand)
    cart = request.session.get('cart')
    
    """
    for t in tshirts:
        #all_sizes = t.sizevariant_set.all()
        min_price = t.sizevariant_set.all().order_by('price').first()
        #print(t , min_price.price, min_price.size)
        t.min_price = min_price.price
        t.after_discount = t.min_price - (t.min_price * t.discount /100)
        t.after_discount = floor(t.after_discount)
    """
    paginator = Paginator(tshirts, 3)
    page_object = paginator.get_page(page)

    query = request.GET.copy()
    query['page'] = ''
    pageurl = urlencode(query)
    

    context = {
        "page_object" : page_object,
        "occasions" : occasions,
        "brands" : brands,
        "neckTypes" : neckTypes,
        "sleeves" : sleeves,
        "colors" : colors,
        "idealFors" : idealFors,
        "pageurl" : pageurl
    }
    return render(request , template_name='store/home.html' , context = context)