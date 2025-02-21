from django.db.models import Q
from rest_framework import mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product, Cart
from .serializer import ProductSerializer

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

api_view(['POST'])
def add_item_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    user = request.user
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product, defaults={'quantity': quantity})
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    return Response({'message': 'Product added to cart'})
