from rest_framework import serializers
from .models import Products


class ProductsFiltersSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    min_price = serializers.IntegerField(required=False)
    max_price = serializers.IntegerField(required=False)


class AddProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField(
        min_value=3000,
        max_value=1_000_000
    )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
