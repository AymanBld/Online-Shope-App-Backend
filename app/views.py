from django.utils import timezone
from django.db.models import Q
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

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
        
        send_mail(
            f'Welcom {serializers.validated_data['username']}',
            f'''Welcom {serializers.validated_data['username']} to AymanShope 
            we are so excited you\'re joining us on this epic journey throught the wonderful world of shopping''',
            None,
            [serializers.validated_data['email']],
            fail_silently=True
        )
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
    
    user.generat_otp()

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

# ---------------------------------- \Home ------------------------------------

@api_view(['GET'])
def list_products_by_category(request, category_id):
    products = Product.objects.filter(category=category_id)
    user = MyUser.objects.filter(id=request.headers.get('user')).first()
    serializer = ProductSerializer(products, many=True, context={'user': user})
    return Response(serializer.data)

@api_view(['GET'])
def list_deal_products(request):
    products = Product.objects.order_by('-discount')
    user = MyUser.objects.filter(id=request.headers.get('user')).first()
    serializer = ProductSerializer(products, many=True, context={'user':user})
    return Response(serializer.data)

@api_view(['GET'])
def search_products_view(request):
    keyword = request.GET.get('product-name')
    user = MyUser.objects.filter(id=request.headers.get('user')).first()
    products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    serializer = ProductSerializer(products, many=True, context={'user':user})
    return Response(serializer.data)

# ---------------------------------- \Favorite ------------------------------------

@api_view(['GET'])
def list_favorite_products(request):
    user = MyUser.objects.filter(id=request.headers.get('user')).first()
    products_favorited = user.favorite_products.all()
    serializer = ProductSerializer(products_favorited, many=True, context={'user': user})
    return Response(serializer.data)

@api_view(['POST', 'DELETE'])
def add_delete_favorite_product(request, product_id):
    user = MyUser.objects.filter(id=request.headers.get('user')).first()
    product = Product.objects.get(id=product_id)

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
        user = MyUser.objects.filter(id=request.headers.get('user')).first()


        cart_item, created = Cart.objects.get_or_create(user=user, product=product, order=None, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            return Response({'message':'cat item incremed'})
        return Response({'message':'cat item created'})

class ListCartView(generics.ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = MyUser.objects.filter(id=self.request.headers.get('user')).first()
        return Cart.objects.filter(user=user, order__isnull=True)

class UpdateRemoveItemCart(generics.DestroyAPIView, generics.UpdateAPIView ):
    serializer_class = CartInputSerializer
    queryset = Cart.objects.all()
    lookup_field = 'id'

@api_view(['POST'])
def check_coupon_view(request):
    name_input = request.data.get('coupon')
    
    if not name_input:
        return Response({'error':'coupon field is required'},status=401)
    coupon = Coupon.objects.filter(name=name_input, quantity__gt=0, dateEx__gte=timezone.now().date()).first()
    
    if not coupon:
        return Response({'error':'invalid coupon code'},status=401)
    
    return Response({'id':coupon.pk, 'discount': coupon.discount, 'name':coupon.name})

# ---------------------------------- \Address ------------------------------------

class AddressListCreatView(generics.ListCreateAPIView):
    serializer_class = AdressSerializer
    def get_queryset(self):
        user = MyUser.objects.filter(id=self.request.headers.get('user')).first()
        return Address.objects.filter(user=user)

class AddressRetriveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdressSerializer
    queryset = Address.objects.all()
    lookup_field = 'id'

# ---------------------------------- \Orders ------------------------------------

class CheckOut(generics.CreateAPIView):
    serializer_class = OrderSerializer      
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        creat_response=self.create(request, *args, **kwargs)
        if creat_response.status_code != status.HTTP_201_CREATED:
            return creat_response

        coupon_id = creat_response.data.get('coupon')
        if coupon_id:
            coupon = Coupon.objects.filter(id=coupon_id).first()
            coupon.quantity -= 1
            coupon.save()
            

        order_id = creat_response.data['id']
        user = MyUser.objects.filter(id=self.request.headers.get('user')).first()
        Cart.objects.filter(order__isnull=True, user=user).update(order=order_id)
        
        return creat_response
        
class ListAllOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = MyUser.objects.filter(id=self.request.headers.get('user')).first()
        return Order.objects.filter(user=user)

class ListActiveOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = MyUser.objects.filter(id=self.request.headers.get('user')).first()
        return Order.objects.filter(user=user)

class RetriveDeleteOrder(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'

class UpdateOrder(generics.UpdateAPIView): #!!!!!!!! just for admin to update status        
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'


