from django.contrib import admin
from django.urls import path
from store.views import home , cart , login, signout, signup, orders, show_prduct, add_to_cart, checkout
from store.views import validatePayment

urlpatterns = [
    path('', home , name= 'homepage'),
    path('cart/', cart ),
    path('orders/', orders),
    path('signup/', signup ),
    path('login/', login, name='login'),
    path('logout/', signout ),
    path('product/<str:slug>' , show_prduct ),
    path('addtocart/<str:slug>/<str:size>' , add_to_cart),
    path('checkout/', checkout ),
    path('validate_payment/', validatePayment ),
]
