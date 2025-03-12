from django.utils import timezone
from django.db.models import Q
from rest_framework import mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .models import *
from .serializer import *

# ---------------------------------- \Auth ------------------------------------

class Registration(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = MyUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializers = UserSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        user.generat_otp()
        # send email
        return Response({'message':'Registartion Succefly'},status=201)

@api_view(['POST'])
def Login(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')

    if not (password and (email or username)):
        return Response({'error':'Email or Username And Password aer requaired'},status=400)
    if username:
        user = MyUser.objects.filter(username=username, password=password).first()
    else:
        user = MyUser.objects.filter(email=email, password=password).first()
    if not user:
        return Response({'error':'Invalid credentials'},status=401)
    
    return Response({
        'message':'Login succesfly',
        'user':{
            'id' : user.pk,
            'username' : user.username,
            'email' : user.email,
            'phone' : user.phone,
            'is_active' : user.is_active
        }
    })
    
@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    username = request.data.get('username')

    if not (email or username):
        return Response({'error':'Email or Username field is required'}, status=400)
    if username:
        user = MyUser.objects.filter(username=username).first()
    else:
        user = MyUser.objects.filter(email=email).first()
    if not user:
        return Response({'error':'Invalid credentials'},status=401)

    # send email to user
    return Response({'message':'Email sent'})

@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    username = request.data.get('username')

    if not (email or username):
        return Response({'error':'Email or Username field is required'}, status=400)
    if username:
        user = MyUser.objects.filter(username=username).first()
    else:
        user = MyUser.objects.filter(email=email).first()
    if not user:
        return Response({'error':'Invalid credentials'},status=401)

    his_otp = request.data.get('otp')
    if not his_otp == user.otp or not user.otp_is_valid():
        return Response({'error':'not verified'}, status=400)
    
    user.is_active = 1
    user.otp = None
    user.otp_created = None
    user.save()
    return Response({'message':'user verified'})

@api_view(['POST'])
def resend_otp_code(request):
    email = request.data.get('email')
    username = request.data.get('username')

    if not (email or username):
        return Response({'error':'Email or Username field is required'}, status=400)
    if username:
        user = MyUser.objects.filter(username=username).first()
    else:
        user = MyUser.objects.filter(email=email).first()
    if not user:
        return Response({'error':'Invalid credentials'},status=401)
    
    user.generat_otp()
    user.save()
    # send another email
    return Response({'message':'email send'})

@api_view(['POST'])
def rest_password(request):
    email = request.data.get('email')
    username = request.data.get('username')

    if not (email or username):
        return Response({'error':'Email or Username field is required'}, status=400)
    if username:
        user = MyUser.objects.filter(username=username).first()
    else:
        user = MyUser.objects.filter(email=email).first()
    if not user:
        return Response({'error':'Invalid credentials'},status=401)
    
    new_password = request.data.get('password')
    user.password = new_password
    user.save()
    return Response({'message':'password reset succesfly'})

# ---------------------------------- \Products ------------------------------------

class ProductsListCreatView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    quezryset = Product.objects.all()

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

# ---------------------------------- \Home ------------------------------------

@api_view(['GET'])
def list_products_by_category(request, category_id):
    products = Product.objects.filter(category=category_id)
    serializer = ProductWithCategorySerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def list_deal_products(request):
    products = Product.objects.order_by('-discount')
    serializer = ProductWithCategorySerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def search_products_view(request):
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

class RetriveDeleteOrder(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer

    queryset = Order.objects.all()
    lookup_field = 'id'

class UpdateOrder(generics.UpdateAPIView): #!!!!!!!! just for admin to update status
    serializer_class = OrderSerializer

    queryset = Order.objects.all()
    lookup_field = 'id'
