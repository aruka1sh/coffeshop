from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import Cart


def cart_detail(request):
    """Просмотр содержимого корзины."""
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
    else:
        if request.session.session_key:
            carts = Cart.objects.filter(session_key=request.session.session_key)
        else:
            carts = []
    return render(request, "shopping_cart/cart_detail.html", {"carts": carts})


def register_user(request):
    """Регистрация нового пользователя."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизуем пользователя после регистрации
            return redirect("cart_detail")
    else:
        form = RegistrationForm()

    return render(request, "shopping_cart/register.html", {"form": form})
