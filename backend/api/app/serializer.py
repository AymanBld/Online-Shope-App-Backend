from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in  obj.favorited_by.all()
        return False