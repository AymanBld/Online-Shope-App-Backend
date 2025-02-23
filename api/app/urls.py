from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/', views.products_of_category),
    path('deals/', views.products_of_deal),
    path('products/', views.search_view),
    path('favorite/', views.list_favorite_products),
    path('favorite/<int:product_id>/', views.add_delete_favorite_product),

    path('cart/', views.ListCart.as_view()),
    path('cart/add/', views.AddItemToCart.as_view()),
]