from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response

from basket.services import get_basket_products
from clients.services import get_client_by_id_or_none
from products.services import get_product_by_id_or_none
from tokens.decorators import check_access_token
from .serializers import OrderPaymentSerializer, OrderSerializer, OrderQuerySerializer, ReturnProductSerializer, \
    OrdersCreationSerializer, OrderProductsSerializer
from .services import get_orders_by_client_id, create_order, save_order_products, get_order_by_id_or_none, \
    calculate_order_amount, get_order_products
from .settings import OrdersStatuses


class OrdersListAPIView(GenericAPIView):
    serializer_class = OrderSerializer

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
        query_serializer=OrderQuerySerializer,
        responses={
            status.HTTP_200_OK: OrderSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    @check_access_token
    def get(self, request):
        serializer = OrderQuerySerializer(data=request.query_params)
        if serializer.is_valid():
            client_id = serializer.validated_data.get('client_id')
            orders = get_orders_by_client_id(client_id)
            orders_serializers = OrderSerializer(orders, many=True)
            return Response(status=status.HTTP_200_OK, data=orders_serializers.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class OrderPaymentAPIView(GenericAPIView):
    serializer_class = OrderPaymentSerializer

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
            status.HTTP_200_OK: OrderProductsSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    @check_access_token
    def patch(self, request):
        serializer = OrderPaymentSerializer(data=request.data)
        if serializer.is_valid():
            client_id = serializer.validated_data.get('client_id')
            order_id = serializer.validated_data.get('order_id')
            client = get_client_by_id_or_none(client_id)
            if client is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'client_id': 'Client not found'
                })
            order = get_order_by_id_or_none(order_id)
            if order is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'order_id': 'Order not found'
                })
            order_amount = calculate_order_amount(order_id)
            if order_amount > client.balance:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'balance': 'Not enough money'
                })
            client.balance -= order_amount
            order.status = OrdersStatuses.PROCESSED.value
            client.save()
            order.save()
            products = get_order_products(order_id)
            products_serializer = OrderProductsSerializer(products, many=True)
            return Response(status=status.HTTP_200_OK, data=products_serializer.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CreateOrderAPIView(GenericAPIView):
    serializer_class = OrdersCreationSerializer

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
            status.HTTP_200_OK: '{"order_id": <order_id_here>}',
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid arguments'
        }
    )
    @check_access_token
    def post(self, request):
        serializer = OrdersCreationSerializer(data=request.data)
        if serializer.is_valid():
            client_id = serializer.validated_data.get('client_id')
            client = get_client_by_id_or_none(client_id)
            if client is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'client_id': 'Client not found'
                })
            order = create_order(client_id)
            basket_products = get_basket_products(client.pk)
            if not basket_products:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'client_id': 'Basket is empty'
                })
            products_ids_list = [basket_product.product.pk for basket_product in basket_products]
            save_order_products(order.pk, products_ids_list)
            return Response(status=status.HTTP_200_OK, data={
                'order_id': order.pk
            })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ReturnProductAPIView(GenericAPIView):
    serializer_class = ReturnProductSerializer

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
    def post(self, request, *args, **kwargs):
        serializer = ReturnProductSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            client_id = serializer.validated_data.get('client_id')

            product = get_product_by_id_or_none(product_id)
            client = get_client_by_id_or_none(client_id)

            if product is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'product_id': 'Product not found'
                })
            if client is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'client_id': 'Client not found'
                })

            client.balance += product.price
            client.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)







