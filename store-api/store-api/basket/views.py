from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from clients.services import is_client_exists
from products.services import get_product_by_id_or_none
from tokens.decorators import check_access_token
from .serializers import BasketProductSerializer, AddBasketProductSerializer, ClearBasketSerializer,\
    BasketProductsListQuerySerializer
from .services import save_basket_product, get_basket_products, clear_basket


class BasketProductsListAPIView(GenericAPIView):
    serializer_class = BasketProductSerializer

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
        query_serializer=BasketProductsListQuerySerializer,
        responses={
            status.HTTP_200_OK: BasketProductSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    @check_access_token
    def get(self, request):
        query_serializer = BasketProductsListQuerySerializer(data=request.query_params)
        if query_serializer.is_valid():
            client_id = query_serializer.validated_data.get('client_id')
            if not is_client_exists(client_id):
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={'client': 'Client not found'})
            basket_products = get_basket_products(client_id)
            products_serializer = BasketProductSerializer(basket_products, many=True)
            return Response(status=status.HTTP_200_OK, data=products_serializer.data)
        return Response(query_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class AddBasketProductAPIView(GenericAPIView):
    serializer_class = AddBasketProductSerializer

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
            status.HTTP_200_OK: 'Success',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid Arguments'
        }
    )
    @check_access_token
    def post(self, request):
        serializer = AddBasketProductSerializer(data=request.data)
        if serializer.is_valid():
            client_id = serializer.validated_data.get('client_id')
            product_id = serializer.validated_data.get('product_id')
            if not is_client_exists(client_id):
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={'client': 'Client not found'})
            product = get_product_by_id_or_none(product_id)
            if product is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={'product': 'Product not found'})
            save_basket_product(client_id, product_id)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ClearBasketAPIView(GenericAPIView):
    serializer_class = ClearBasketSerializer

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
            status.HTTP_200_OK: 'Success',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid Arguments'
        }
    )
    @check_access_token
    def post(self, request):
        serializer = ClearBasketSerializer(data=request.data)
        if serializer.is_valid():
            client_id = serializer.validated_data.get('client_id')
            if not is_client_exists(client_id):
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={'client_id': 'Client not found'})
            clear_basket(client_id)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
