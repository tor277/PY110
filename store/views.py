from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.shortcuts import render, redirect
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
                if data['html'] == page:
                    data_category = filtering_category(DATABASE, category_key=data['category'])
                    data_category.remove(data)
                    return render(request, "store/product.html", context={"product": data,
                                                                          'prod_category': data_category[:5]})
                    #
                    # with open(f'store/products/{page}.html', 'r', encoding='utf=8') as f:
                    #     data = f.read()
                    # return HttpResponse(data)
        elif isinstance(page, int):
            # if str(page) in DATABASE:
            #     with open(f'store/products/{DATABASE[str(page)]["html"]}.html', 'r', encoding='utf=8') as f:
            #         data = f.read()
            #     return HttpResponse(data)
            data = DATABASE[str(page)]  # Получаем какой странице соответствует данный id
            if data:
                data_category = filtering_category(DATABASE, category_key=data['category'])
                data_category.remove(data)
                return render(request, "store/product.html", context={"product": data,
                                                                      'prod_category': data_category[:5]})
        return HttpResponse(status=404)

def shop_view(request):
    # if request.method == 'GET':
    #     # with open('store/shop.html', 'r', encoding='utf-8') as f:
    #     #     data = f.read()
    #     # return HttpResponse(data)
    #     return render(request, 'store/shop.html', context={'products': DATABASE.values()})
    if request.method == "GET":
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'store/shop.html',
                      context={"products": data,
                               "category": category_key})

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

def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    # print(name_coupon)
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        # TODO Проверьте, что купон есть в DATA_COUPON, если он есть, то верните JsonResponse в котором по ключу "discount"
        # получают значение скидки в процентах, а по ключу "is_valid" понимают действителен ли купон или нет (True, False)
        if name_coupon in DATA_COUPON:
            coupon = DATA_COUPON[name_coupon]
            return JsonResponse({
                'is_valid': coupon['is_valid'],
                'discount': coupon['value']
            })
        return HttpResponseNotFound('Неверный купон!')


        # TODO Если купона нет в базе, то верните HttpResponseNotFound("Неверный купон")

def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 50},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if country in DATA_PRICE:
            if city in DATA_PRICE[country]:
               return JsonResponse({'price': DATA_PRICE[country][city]['price']})
            else:
                return JsonResponse({'price': DATA_PRICE[country]['fix_price']})
        return HttpResponseNotFound("Неверные данные!")
        # TODO Реализуйте логику расчёта стоимости доставки, которая выполняет следующее:
        # Если в базе DATA_PRICE есть и страна (country) и существует город(city), то вернуть JsonResponse со словарём, {"price": значение стоимости доставки}
        # Если в базе DATA_PRICE есть страна, но нет города, то вернуть JsonResponse со словарём, {"price": значение фиксированной стоимости доставки}
        # Если нет страны, то вернуть HttpResponseNotFound("Неверные данные")

def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")