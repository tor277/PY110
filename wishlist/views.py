from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from store.models import DATABASE


# Create your views here.
@login_required(login_url='login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]
        if request.GET.get('format') in ('json', 'JSON'):
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []  # Список продуктов
        for product_id in data['products']:
            product = DATABASE.get(product_id)  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            # product['quantity'] = quantity
            # product["price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            # product['price_total'] = str(round(quantity * product['price_after'], 2))
            # 3. добавьте product в список products
            products.append(product)
        # return render(request, "store/cart.html", context={"products": products})
        # return render(request, "wishlist/wishlist.html")
        return render(request, "wishlist/wishlist.html", context={"products": products})
# @login_required(login_url='login:login_view')
def wishlist_add_json(request, id_product: str):
    if request.method == "GET":
        result = add_to_wishlist(request, id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт теперь избранный"},
                                json_dumps_params={'ensure_ascii': False, 'indent': 4})

        return JsonResponse({"answer": "Неудачное добавление в избранное"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
# @login_required(login_url='login:login_view')
def wishlist_del_json(request, id_product: str):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт больше не избранный"},
                                json_dumps_params={'ensure_ascii': False, 'indent': 4
                                                   })

        return JsonResponse({"answer": "Неудачное удаление из избранного"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def wishlist_json(request):
    if request.method == "GET":
        current_user = get_user(request).username  # from django.contrib.auth import get_user
        data = view_in_wishlist(request)[current_user]  # TODO получите данные о списке товаров в избранном у пользователя
        if data:
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})  # TODO верните JsonResponse c data
        return JsonResponse({"answer": "Пользователь не авторизирован"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})  # TODO верните JsonResponse с ключом "answer" и значением "Пользователь не авторизирован" и параметром status=404


def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        result = wishlist_del_json(request, id_product)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("wishlist:wishlist_view")  # TODO Вернуть перенаправление на корзину

