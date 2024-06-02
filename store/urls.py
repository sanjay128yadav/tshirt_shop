from django.contrib import admin
from django.urls import path
from store.views import home , cart , login, signout, signup, orders, show_prduct

urlpatterns = [
    path('', home , name= 'homepage'),
    path('cart/', cart ),
    path('orders/', orders ),
    path('signup/', signup ),
    path('login/', login ),
    path('logout/', signout ),
    path('product/<str:slug>' , show_prduct )
]
