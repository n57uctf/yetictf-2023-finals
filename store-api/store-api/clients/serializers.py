from rest_framework import serializers
from .models import Clients


class ClientQuerySerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'


class UpgradeClientStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()

