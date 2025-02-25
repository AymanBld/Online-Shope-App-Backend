from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductsListCreatView.as_view()),
    path('products/<int:id>', ProductsRetriveView.as_view()),

    path('category/<int:category_id>/', list_products_from_category),
    path('deals/', list_deal_products),
    # path('products/', search_view),
    path('favorite/', list_favorite_products),
    path('favorite/<int:product_id>/', add_delete_favorite_product),

    path('cart/', ListCartView.as_view()),
    path('cart/add/', AddItemCartView.as_view()),
    path('cart/<int:id>/', UpdateRemoveItemCart.as_view()),   # Allowed: DELETE - PATCH 
    path('cart/coupon/', check_coupon_view),

    path('orders/', CreatOrderView.as_view()),
    path('orders/active/', ListActiveOrdersView.as_view()),
    path('orders/archive/', ListAllOrdersView.as_view()),
    path('orders/<int:id>/', RetriveDeleteUpdateOrder.as_view()),

    path('address/', AddressListCreatView.as_view()),
    path('address/<int:id>/', AddressRetriveView.as_view()),
]