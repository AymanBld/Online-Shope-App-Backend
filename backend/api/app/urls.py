from django.urls import path
from .views import products_of_category, products_of_deal

urlpatterns = [
    # path('product/', ProductView.as_view()),
    path('categories/<int:category_id>/', products_of_category),
    path('deals/', products_of_deal),
  
]