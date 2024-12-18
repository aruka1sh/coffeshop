from django.shortcuts import render
from django.http import HttpResponse
from .models import Coffee

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
