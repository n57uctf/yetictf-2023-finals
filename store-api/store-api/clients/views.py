from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tokens.decorators import check_access_token
from .serializers import ClientSerializers, ClientQuerySerializer, UpgradeClientStatusSerializer
from .services import get_client_by_id_or_none, upgrade_client_status_to_premium
from .settings import PREMIUM_STATUS_PRICE, ClientsStatuses


class ClientAPIView(APIView):
    serializer_class = ClientSerializers

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                'Access token',
                type=openapi.TYPE_STRING),
        ],
        query_serializer=ClientQuerySerializer,
        responses={
            status.HTTP_200_OK: ClientSerializers(),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid arguments'
        }
    )
    @check_access_token
    def get(self, request):
        serializer = ClientQuerySerializer(data=request.query_params)
        if serializer.is_valid():
            id_ = serializer.validated_data.get('id')
            client = get_client_by_id_or_none(id_)
            if client is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={'client_id': 'Client not found'})
            client_serializer = ClientSerializers(client)
            return Response(status=status.HTTP_200_OK, data=client_serializer.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UpgradeClientStatusAPIView(GenericAPIView):
    serializer_class = UpgradeClientStatusSerializer

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                'Access token',
                type=openapi.TYPE_STRING),
        ],
        responses={
            status.HTTP_200_OK: ClientSerializers(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid arguments'
        }
    )
    @check_access_token
    def patch(self, request):
        serializer = UpgradeClientStatusSerializer(data=request.data)
        if serializer.is_valid():
            client_id = serializer.validated_data.get('id')
            client = get_client_by_id_or_none(client_id)
            if client is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'client_id': 'Client not found'})
            if client.status == ClientsStatuses.PREMIUM.value:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={'client': 'Client already premium'})
            if client.balance < PREMIUM_STATUS_PRICE:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={'balance': 'Not enough money'})
            upgrade_client_status_to_premium(client_id)
            client.balance -= PREMIUM_STATUS_PRICE
            client.status = ClientsStatuses.PREMIUM.value
            client.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

