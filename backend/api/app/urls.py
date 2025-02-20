from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/', views.products_of_category),
    path('deals/', views.products_of_deal),
    path('products/', views.search_view),
]