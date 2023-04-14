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


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()


class ProductCreationSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()


class DateTimeSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class ProductsListSerializer(serializers.Serializer):
    product = ProductSerializer()
    key_info = DateTimeSerializer()


