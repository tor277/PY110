from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.shortcuts import render


# Create your views here.
def products_view(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            if id in DATABASE:
                return JsonResponse(DATABASE[id],
                                    json_dumps_params={'indent': 4, 'ensure_ascii': False})
            return HttpResponseNotFound('<h1>Данного продукта <u>нет</u> в <u>БАЗЕ ДАННЫХ</u>, а значит и на ОВОЩЕБАЗЕ =)</h1>')
        return JsonResponse(DATABASE,
                            json_dumps_params={'indent': 4, 'ensure_ascii': False})

def shop_view(request):
    if request.method == 'GET':
        with open('store/shop.html', 'r', encoding='utf-8') as f:
            data = f.read()
        return HttpResponse(data)