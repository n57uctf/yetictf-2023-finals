from rest_framework import serializers


class PutFlagSerializer(serializers.Serializer):
    round_number = serializers.IntegerField()
    flag = serializers.CharField()


class PullFlagSerializer(serializers.Serializer):
    private_info = serializers.CharField()
    flag = serializers.CharField()
