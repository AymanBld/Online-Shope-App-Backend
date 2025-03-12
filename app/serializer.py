from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'discount', 'image_url', 'category']

class ProductWithCategorySerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image_url', 'price', 'discount', 'is_favorite', 'dicountedPrice', 'category']  

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user :
            return user in obj.favorited_by.all()
        return False
    

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Cart
        # fields = ['id', 'product', 'quantity']
        fields = '__all__'

class CartInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product', 'quantity']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class AdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
