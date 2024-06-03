from django.contrib import admin
from django.urls import path
from store.views import home , cart , login, signout, signup, orders, show_prduct, add_to_cart

urlpatterns = [
    path('', home , name= 'homepage'),
    path('cart/', cart ),
    path('orders/', orders ),
    path('signup/', signup ),
    path('login/', login ),
    path('logout/', signout ),
    path('product/<str:slug>' , show_prduct ),
    path('addtocart/<str:slug>/<str:size>' , add_to_cart)
]
