from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product
from .serializer import ProductSerializer

@api_view(['GET'])
def products_of_category(request, category_id):
    products = Product.objects.filter(category=category_id).order_by('favorited_by')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def products_of_deal(request):
    products = Product.objects.order_by('-discount')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_view(request):
    keyword = request.GET.get('keyword')
    products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)