from django.urls import path

from wishlist.views import wishlist_view, wishlist_add_json, wishlist_del_json, wishlist_json, wishlist_remove_view

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_view, name="wishlist_view"),
    path('api/add/<str:id_product>', wishlist_add_json),
    path('api/del/<str:id_product>', wishlist_del_json),
    path('/remove/<str:id_product>', wishlist_remove_view, name="remove_from_wishlist"),
    path('api/', wishlist_json, name="wishlist_json"),
    ]