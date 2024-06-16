from django.contrib import admin
from django.urls import path
from store.views import home , cart , LoginView, signout, signup, orders, add_to_cart, checkout
from store.views import validatePayment, ProductDetailView

urlpatterns = [
    path('', home , name= 'homepage'),
    path('cart/', cart ),
    path('orders/', orders),
    path('signup/', signup ),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', signout ),
    path('product/<str:slug>' , ProductDetailView.as_view() ),
    path('addtocart/<str:slug>/<str:size>' , add_to_cart),
    path('checkout/', checkout ),
    path('validate_payment/', validatePayment ),
]
