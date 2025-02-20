from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'discount', 'image_url', 'category', 'is_favorite']  

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        return user in obj.favorited_by.all()
