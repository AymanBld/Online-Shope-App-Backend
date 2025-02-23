from .models import Product, Category, Cart
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image_url', 'price', 'discount', 'is_favorite', 'category']  

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        return user in obj.favorited_by.all()
    
class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']

class CartInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
