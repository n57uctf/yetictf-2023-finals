from rest_framework import serializers
from .models import PromoCodes


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCodes
        fields = '__all__'


class PromoCodesActivationSerializer(serializers.Serializer):
    promo_code = serializers.CharField()
    client_id = serializers.IntegerField()




