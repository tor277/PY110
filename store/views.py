from django.http import HttpResponse, JsonResponse
from .models import DATABASE
from django.shortcuts import render


# Create your views here.
def products_view(request):
    if request.method == 'GET':
        return JsonResponse(DATABASE,
                            json_dumps_params={'indent': 4, 'ensure_ascii': False})

def shop_view(request):
    if request.method == 'GET':
        with open('store/shop.html', 'r', encoding='utf-8') as f:
            data = f.read()
        return HttpResponse(data)