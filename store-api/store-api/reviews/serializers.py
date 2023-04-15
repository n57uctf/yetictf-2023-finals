from rest_framework import serializers
from .models import Reviews


class ReviewsQuerySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    client_id = serializers.IntegerField(required=False)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class LeaveReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    client_id = serializers.IntegerField()
    text = serializers.CharField()
    rating = serializers.IntegerField(min_value=0, max_value=5)





