from django.utils import timezone
from django.db.models import Q
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Product, Cart, Coupon
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
        return Cart.objects.filter(user=user)
        

class AddItemCart(generics.GenericAPIView):
    serializer_class = CartInputSerializer
    def post(self, request, *arg, **kwarg):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        user = request.user
        cart_item, created = Cart.objects.get_or_create(user=user, product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            
            cart_item.save()
            return Response({'message':'cat item incremed'})
        return Response({'message':'cat item created'})

class UpdateRemovwItemCart(generics.DestroyAPIView, mixins.UpdateModelMixin):
    serializer_class = CartInputSerializer
    queryset = Cart.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data['quantity']
        if quantity > 0:
            serializer.save()
            return Response(serializer.data)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def check_coupon(request):
    name_input = request.GET.get('coupon')
    coupon = get_object_or_404(Coupon, name=name_input, quantity__gt=0, dateEx__gte=timezone.now().date())
    return Response({'discount': coupon.discount})
