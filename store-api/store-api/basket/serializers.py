from rest_framework import serializers
from .models import BasketProducts


class BasketProductsListQuerySerializer(serializers.Serializer):
    client_id = serializers.IntegerField()


class BasketProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketProducts
        fields = '__all__'


class AddBasketProductSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    product_id = serializers.IntegerField()


class ClearBasketSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()


