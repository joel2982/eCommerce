from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('cart', views.cart, name = 'cart'),
    path('checkout_address', views.checkout_address, name = 'checkout_address'),
    path('add_product', views.add_product, name = 'add_product'),
    path('product_desc/<int:pk>', views.product_desc, name = 'product_desc'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name = 'remove_from_cart'),
] 
