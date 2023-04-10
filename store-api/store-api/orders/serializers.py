from rest_framework import serializers

from products.models import Products
from .models import Orders, OrderProducts


class OrderQuerySerializer(serializers.Serializer):
    client_id = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class OrderPaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    client_id = serializers.IntegerField()


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class ReturnProductSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    product_id = serializers.IntegerField()


class OrdersCreationSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()


