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


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page,str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
            # TODO 1. Откройте файл open(f'store/products/{page}.html', encoding="utf-8") (Не забываем про контекстный менеджер with)
            # TODO 2. Прочитайте его содержимое
            # TODO 3. Верните HttpResponse c содержимым html файла
                    with open(f'store/products/{page}.html', 'r', encoding='utf=8') as f:
                        data = f.read()
                        return HttpResponse(data)
        elif isinstance(page, int):
            if str(page) in DATABASE:
                with open(f'store/products/{DATABASE[str(page)]["html"]}.html', 'r', encoding='utf=8') as f:
                    data = f.read()
                return HttpResponse(data)
        # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
        # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
        return HttpResponse(status=404)

def shop_view(request):
    if request.method == 'GET':
        with open('store/shop.html', 'r', encoding='utf-8') as f:
            data = f.read()
        return HttpResponse(data)