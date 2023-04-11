from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from tokens.jwt import JWT
from tokens.services import create_refresh_token, get_refresh_token_or_none
from clients.models import Clients
from .serializers import ClientAuthenticationSerializer


class ClientAuthenticationAPIView(GenericAPIView):
    serializer_class = ClientAuthenticationSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Client authenticated',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_304_NOT_MODIFIED: 'Already authorized',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid parameters'
        }
    )
    def post(self, request):
        data = request.data
        auth_serializer = ClientAuthenticationSerializer(data=data)
        if auth_serializer.is_valid():
            try:
                user = auth_serializer.get_client()
                refresh_token = get_refresh_token_or_none(user.pk)
                if refresh_token is not None:
                    return Response(status=status.HTTP_304_NOT_MODIFIED)
                jwt = JWT({
                    'user_id': user.pk
                })
                create_refresh_token(client_id=user.pk, token=jwt.refresh_token)
                return Response(status=status.HTTP_200_OK, data=jwt.as_dict())
            except Clients.DoesNotExist:
                return Response({
                    'password': 'Invalid password'
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(auth_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

