from django.urls import path, include
from .views import *

urlpatterns = [
    # Authentication: ---------------------------------------------------------------------------------
    path('auth/registration/', Registration.as_view()),
    path('auth/login/', Login),
    path('auth/verify/', verify_otp),
    path('auth/resend-email/', resend_otp_code),
    path('auth/password/forget/', forgot_password),
    path('auth/password/reset/', rest_password),
    
    # For Admin: ---------------------------------------------------------------------------------
    path('products/', ProductsListCreatView.as_view()),
    path('products/<int:id>', ProductsRetriveView.as_view()),

    path('category/', CategoryListCreatView.as_view()),
    path('category/<int:id>', CategoryRetriveView.as_view()),

    path('orders/<int:id>', UpdateOrder.as_view()),

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
    path('cart/checkout/', CheckOut.as_view()),

    path('orders/<int:id>/', RetriveDeleteOrder.as_view()),
    path('orders/active/', ListActiveOrdersView.as_view()),
    path('orders/archive/', ListAllOrdersView.as_view()),

    path('address/', AddressListCreatView.as_view()),
    path('address/<int:id>/', AddressRetriveView.as_view()),
]