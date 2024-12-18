from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),  # Страница корзины
    path('register/', views.register_user, name='register_user'),  # Регистрация пользователя
]
