from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.shortcuts import render
from logic.services import filtering_category, view_in_cart, add_to_cart, remove_from_cart


# Create your views here.
def products_view(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            if id in DATABASE:
                return JsonResponse(DATABASE[id],
                                    json_dumps_params={'indent': 4, 'ensure_ascii': False})
            return HttpResponseNotFound('<h1>Данного продукта <u>нет</u> в <u>БАЗЕ ДАННЫХ</u>, а значит и на ОВОЩЕБАЗЕ =)</h1>')
        category_key = request.GET.get('category')
        orderin_key = request.GET.get('ordering')
        if orderin_key:
            if request.GET.get('reverse') in ['true', 'TRUE', 'True']:
                data = filtering_category(DATABASE, category_key, orderin_key, True)
            else:
                data = filtering_category(DATABASE, category_key, orderin_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return JsonResponse(data,
                            json_dumps_params={'indent': 4, 'ensure_ascii': False},
                            safe=False)


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
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
        # with open('store/shop.html', 'r', encoding='utf-8') as f:
        #     data = f.read()
        # return HttpResponse(data)
        return render(request, 'store/shop.html', context={'products': DATABASE.values()})

def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        if request.GET.get('format') in ('json', 'JSON'):
            # data = view_in_cart() # TODO Вызвать ответственную за это действие функцию
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE.get(product_id)  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product['quantity'] = quantity
            # product["price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            product['price_total'] = str(round(quantity * product['price_after'], 2))
            # 3. добавьте product в список products
            products.append(product)
        return render(request, "store/cart.html", context={"products": products})



def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False, 'indent': 4})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False, 'indent': 4
                                                   })

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})