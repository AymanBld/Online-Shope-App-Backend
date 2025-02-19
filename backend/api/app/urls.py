from django.urls import path
from .views import products_of_category

urlpatterns = [
    # path('product/', ProductView.as_view()),
    path('categories/<int:category_id>/', products_of_category),
  
]