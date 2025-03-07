from django.urls import path
from .views import *

urlpatterns = [
    # For Admin: ---------------------------------------------------------------------------------
    path('products/', ProductsListCreatView.as_view()),
    path('products/<int:id>', ProductsRetriveView.as_view()),

    path('category/', CategoryListCreatView.as_view()),
    path('category/<int:id>', CategoryRetriveView.as_view()),

    # For users: ---------------------------------------------------------------------------------
    path('products/category/<int:category_id>/', list_products_by_category),
    path('products/deals/', list_deal_products),
    path('products/search/', search_products_view),

    path('favorite/', list_favorite_products),
    path('favorite/<int:product_id>/', add_delete_favorite_product),

    path('cart/', ListCartView.as_view()),
    path('cart/add/', AddItemCartView.as_view()),
    path('cart/<int:id>/', UpdateRemoveItemCart.as_view()),   # Allowed: DELETE - PATCH 
    path('cart/coupon/', check_coupon_view),

    path('orders/', CreatOrderView.as_view()),
    path('orders/active/', ListActiveOrdersView.as_view()),
    path('orders/archive/', ListAllOrdersView.as_view()),
    path('orders/<int:id>/', RetriveDeleteOrder.as_view()),

    path('address/', AddressListCreatView.as_view()),
    path('address/<int:id>/', AddressRetriveView.as_view()),
]