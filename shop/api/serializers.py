from rest_framework import serializers
from shop.models import Product,Category,CartItem,Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'



