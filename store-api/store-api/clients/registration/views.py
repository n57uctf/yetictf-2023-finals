"""
This module contains APIView class for clients registration
"""
from django.db.utils import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import ClientRegistrationSerializer, ClientSerializer


class ClientsRegistrationAPIView(GenericAPIView):
    serializer_class = ClientRegistrationSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: ClientSerializer(),
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid arguments'
        }
    )
    def post(self, request):
        data = request.data.copy()
        client_serializer = ClientRegistrationSerializer(data=data)
        if client_serializer.is_valid():
            try:
                client = client_serializer.save()
                serializer = ClientSerializer(client)
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            except IntegrityError:
                return Response({
                    'email': 'Email already in use'
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(client_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

