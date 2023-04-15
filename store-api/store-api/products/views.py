from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from tokens.decorators import check_access_token
from secretkeys.services import save_secret_key, generate_random_string, encode_string
from .models import Products
from .serializers import ProductSerializer, ProductsFiltersSerializer, AddProductSerializer, \
    ProductsListSerializer, DateTimeSerializer
from .services import save_product
from secretkeys.services import get_secret_key_by_product_id_or_none


class ProductsListAPIView(ListAPIView):
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
        query_serializer=ProductsFiltersSerializer,
        responses={
            status.HTTP_200_OK: ProductsListSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid parameters'
        }
    )
    @check_access_token
    def get(self, request, *args, **kwargs):
        serializer = ProductsFiltersSerializer(data=request.query_params)
        if serializer.is_valid():
            parameters = dict()
            min_price = self.request.query_params.get('min_price')
            max_price = self.request.query_params.get('max_price')
            pk = self.request.query_params.get('id')
            if min_price is not None and min_price.isdigit():
                parameters['price__gte'] = min_price
            if max_price is not None and max_price.isdigit():
                parameters['price__lte'] = max_price
            if pk is not None:
                parameters['pk'] = pk
            products = Products.objects.filter(**parameters)
            response_data = list()
            for product in products:
                secret_key = get_secret_key_by_product_id_or_none(product.pk)
                if secret_key is None:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                        'product': 'Secret key is not specified'
                    })
                key_info_serializer = DateTimeSerializer(data={
                    'created_at': secret_key.created_at,
                    'updated_at': secret_key.updated_at
                })
                if not key_info_serializer.is_valid():
                    return Response(key_info_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                product_serializer = ProductSerializer(data={
                    'id': product.pk,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price
                })
                if not product_serializer.is_valid():
                    return Response(product_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                list_serializer = ProductsListSerializer(data={
                        'product': product_serializer.data,
                        'key_info': key_info_serializer.data
                    })
                if not list_serializer.is_valid():
                    return Response(list_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                response_data.append(list_serializer.data)
            response_serializer = ProductsListSerializer(data=response_data, many=True)
            if not response_serializer.is_valid():
                return Response(response_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return Response(status=status.HTTP_200_OK, data=response_serializer.data)
        return Response(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)


class AddProductAPIView(GenericAPIView):
    serializer_class = AddProductSerializer

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: '{"product_id": int, "secret_key": str}',
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    @check_access_token
    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            description = serializer.validated_data.get('description')
            price = serializer.validated_data.get('price')
            secret_key = generate_random_string()
            encoded_description = encode_string(description, secret_key)
            product = save_product(name, encoded_description, price)
            save_secret_key(secret_key, product.pk)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'product_id': product.pk,
                    'secret_key': secret_key
                }
            )
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


