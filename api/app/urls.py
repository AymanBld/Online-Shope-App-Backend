from django.urls import path
from .views import *

urlpatterns = [
    path('category/<int:category_id>/', products_of_category),
    path('deals/', products_of_deal),
    path('products/', search_view),
    path('favorite/', list_favorite_products),
    path('favorite/<int:product_id>/', add_delete_favorite_product),

    path('cart/', ListCart.as_view()),
    path('cart/add/', AddItemCart.as_view()),
    path('cart/<int:id>/', UpdateRemovwItemCart.as_view()),
    path('cart/coupon/', check_coupon),
]