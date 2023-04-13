from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from tokens.decorators import check_access_token
from secretkeys.services import save_secret_key, generate_random_string, encode_string
from .models import Products
from .serializers import ProductSerializer, ProductsFiltersSerializer, AddProductSerializer
from .services import save_product


class ProductsListAPIView(ListAPIView):
    serializer_class = ProductSerializer

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
            status.HTTP_200_OK: ProductSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid parameters'
        }
    )
    @check_access_token
    def get(self, request, *args, **kwargs):
        serializer = ProductsFiltersSerializer(data=request.query_params)
        if serializer.is_valid():
            return super().get(request, *args, **kwargs)
        return Response(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_queryset(self):
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
        queryset = Products.objects.filter(**parameters)
        return queryset


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
        serializer = ProductSerializer(data=request.data)
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


