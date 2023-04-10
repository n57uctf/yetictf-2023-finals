from rest_framework import serializers
from clients.models import Clients
from clients.registration.services import make_sha256_hash


class ClientAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def get_client(self) -> Clients:
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        password = make_sha256_hash(password)
        return Clients.objects.get(email=email, password=password)

