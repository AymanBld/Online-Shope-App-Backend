from django.db.models import Q
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Product, Cart
from .serializer import *


@api_view(['GET'])
def products_of_category(request, category_id):
    products = Product.objects.filter(category=category_id).order_by('favorited_by')
    
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def products_of_deal(request):
    products = Product.objects.order_by('-discount')
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def search_view(request):
    keyword = request.GET.get('keyword')
    products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

# ---------------- \Favorite Products ------------

@api_view(['GET'])
def list_favorite_products(request):
    user = request.user
    products_favorited = user.favorite_products.all()
    serializer = ProductSerializer(products_favorited, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST', 'DELETE'])
def add_delete_favorite_product(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if request.method == 'POST':
        product.favorited_by.add(user)
        return Response({'message': 'Product added to favorites'})
    if request.method == 'DELETE':
        product.favorited_by.remove(user)
        return Response({'message': 'Product removed from favorites'})

# ---------------------- \Cart ------------------------

class ListCart(generics.ListAPIView):
    serializer_class = CartSerializer
    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user)
        return queryset

class AddItemToCart(generics.GenericAPIView):
    serializer_class = CartInputSerializer
    def post(self, request, *arg, **kwarg):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        user = request.user
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return Response(serializer.data)
            
