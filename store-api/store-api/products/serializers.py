from rest_framework import serializers
from .models import Products, ProductsReviews


class ProductsFiltersSerializer(serializers.Serializer):
    min_price = serializers.IntegerField(required=False)
    max_price = serializers.IntegerField(required=False)


class PremiumProductsFiltersSerializer(ProductsFiltersSerializer):
    client_id = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('pk', 'name', 'description', 'price', 'is_premium')


class ProductsReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsReviews
        fields = '__all__'


class ProductsReviewsQuerySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    client_id = serializers.IntegerField(required=False)


class LeaveProductReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    client_id = serializers.IntegerField()
    text = serializers.CharField()
    rating = serializers.IntegerField(min_value=0, max_value=5)


