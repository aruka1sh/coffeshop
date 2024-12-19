from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('location/', views.location, name='location'),
    path('add-to-cart/<int:coffee_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('api/cart/', views.get_cart_items, name='get_cart_items'),
]