from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Coffee, Cart, CartItem
from django.views.decorators.csrf import csrf_exempt

def home(request):
    print(request)
    query = request.GET.get('q', '')  # Получаем параметр `q` из URL
    if query:
        # Фильтруем кофе, если есть поисковый запрос
        coffee = Coffee.objects.filter(name__icontains=query)
    else:
        # Если запроса нет, отображаем все кофе
        coffee = Coffee.objects.all()
    return render(request, 'home.html', {'coffee': coffee, 'query': query})

def location(request):
    return render(request, 'location.html')

def add_to_cart(request, coffee_id):
    coffee = get_object_or_404(Coffee, id=coffee_id)
    # Получаем или создаем корзину
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    
    # Добавляем товар в корзину или увеличиваем количество
    cart_item, created = CartItem.objects.get_or_create(cart=cart, coffee=coffee)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('home')

def get_cart_items(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart = Cart.objects.filter(session_key=request.session.session_key).first()

    items = []
    if cart:
        items = [
            {
                'id': item.id,  # Уникальный ID элемента корзины
                'name': item.coffee.name,
                'price': item.coffee.price,
                'quantity': item.quantity,
                'total_price': item.total_price()
            } for item in cart.items.all()
        ]
    return JsonResponse({'items': items})

@csrf_exempt
def remove_from_cart(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse({'status': 'error', 'message': 'Session not found.'})
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__session_key=session_key)

    cart_item.delete()
    return JsonResponse({'status': 'success', 'message': 'Item removed from cart.'})