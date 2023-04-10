from rest_framework.generics import  GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from tokens.decorators import check_access_token
from .serializers import PromoCodesActivationSerializer, PromoCodeSerializer
from .services import get_all_promo_codes, get_promo_code_or_none, save_promo_code_activation
from clients.services import get_client_by_id_or_none, top_up_client_balance


class PromoCodesListAPIView(GenericAPIView):
    serializer_class = PromoCodeSerializer

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
            status.HTTP_200_OK: 'Product returned successfully',
            status.HTTP_403_FORBIDDEN: 'Access denied',
        }
    )
    @check_access_token
    def get(self, request):
        promo_codes = get_all_promo_codes()
        promo_codes_serializer = PromoCodeSerializer(promo_codes, many=True)
        return Response(status=status.HTTP_200_OK, data=promo_codes_serializer.data)


class ActivatePromoCodeAPIView(GenericAPIView):
    serializer_class = PromoCodesActivationSerializer

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
            status.HTTP_200_OK: 'Product returned successfully',
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid arguments'
        }
    )
    @check_access_token
    def post(self, request):
        serializer = PromoCodesActivationSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('promo_code')
            client_id = serializer.validated_data.get('client_id')
            client = get_client_by_id_or_none(client_id)
            if client is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={'client_id': 'Client not found'})
            promo_code = get_promo_code_or_none(code)
            if promo_code is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={'promo_code': 'Promocode not found'})
            top_up_client_balance(client_id, promo_code.amount)
            save_promo_code_activation(client_id, promo_code.pk)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)




