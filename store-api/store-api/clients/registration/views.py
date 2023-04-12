"""
This module contains APIView class for clients registration
"""
from django.db.utils import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from tokens.jwt import JWT
from tokens.services import create_refresh_token
from .serializers import ClientRegistrationSerializer


class ClientsRegistrationAPIView(GenericAPIView):
    serializer_class = ClientRegistrationSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Client created',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'client_id': openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid arguments'
        }
    )
    def post(self, request):
        data = request.data.copy()
        client_serializer = ClientRegistrationSerializer(data=data)
        if client_serializer.is_valid():
            try:
                client = client_serializer.save()
                jwt = JWT({
                    'user_id': client.pk
                })
                create_refresh_token(client_id=client.id, token=jwt.refresh_token)
                response_data = jwt.as_dict()
                response_data['client_id'] = client.pk
                return Response(status=status.HTTP_201_CREATED, data=response_data)
            except IntegrityError:
                return Response({
                    'email': 'Email already in use'
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(client_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

