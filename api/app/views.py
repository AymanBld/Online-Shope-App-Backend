from django.utils import timezone
from django.db.models import Q
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import *
from .serializer import *

# ---------------------------------- \Products ------------------------------------

class ProductsListCreatView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductsRetriveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

# ---------------------------------- \Category ------------------------------------

class CategoryListCreatView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryRetriveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'

# ---------------------------------- \Products ------------------------------------

@api_view(['GET'])
def list_products_from_category(request, category_id):
    products = Product.objects.filter(category=category_id).order_by('favorited_by')
    
    serializer = ProductWithCategorySerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def list_deal_products(request):
    products = Product.objects.order_by('-discount')
    serializer = ProductWithCategorySerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def search_view(request):
    keyword = request.GET.get('keyword')
    products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    serializer = ProductWithCategorySerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

# ---------------------------------- \Favorite ------------------------------------

@api_view(['GET'])
def list_favorite_products(request):
    user = request.user
    products_favorited = user.favorite_products.all()
    serializer = ProductWithCategorySerializer(products_favorited, many=True, context={'request': request})
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

# ---------------------------------- \Cart ------------------------------------

class AddItemCartView(generics.GenericAPIView):
    serializer_class = CartInputSerializer
    def post(self, request, *arg, **kwarg):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        user = request.user

        cart_item, created = Cart.objects.get_or_create(user=user, product=product, order=None, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            return Response({'message':'cat item incremed'})
        return Response({'message':'cat item created'})

class ListCartView(generics.ListAPIView):
    serializer_class = CartSerializer
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

class UpdateRemoveItemCart(generics.DestroyAPIView, mixins.UpdateModelMixin):
    serializer_class = CartInputSerializer
    queryset = Cart.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        if request.data.get('quantity') > 0:
            return self.partial_update(request, *args, **kwargs)
        return self.destroy(request, *args, **kwargs)

@api_view(['GET'])
def check_coupon_view(request):
    name_input = request.GET.get('coupon')
    coupon = get_object_or_404(Coupon, name=name_input, quantity__gt=0, dateEx__gte=timezone.now().date())
    return Response({'discount': coupon.discount})

# ---------------------------------- \Address ------------------------------------

class AddressListCreatView(generics.ListCreateAPIView):
    serializer_class = AdressSerializer
    queryset = Address.objects.all()

class AddressRetriveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdressSerializer
    queryset = Address.objects.all()
    lookup_field = 'id'

# ---------------------------------- \Orders ------------------------------------

class CreatOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer      
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        creat_response=self.create(request, *args, **kwargs)
        order_id = creat_response.data['id']

        user = request.user
        Cart.objects.filter(order__isnull=True, user=user).update(order=order_id)
        return creat_response
        
class ListAllOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class ListActiveOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(status__lt=4)

class RetriveDeleteUpdateOrder(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'