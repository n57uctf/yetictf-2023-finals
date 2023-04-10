from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from clients.services import get_client_by_id_or_none, top_up_client_balance
from clients.settings import ClientsStatuses
from tokens.decorators import check_access_token
from .models import Products
from .serializers import ProductSerializer, ProductsFiltersSerializer, PremiumProductsFiltersSerializer, \
    ProductsReviewSerializer, ProductsReviewsQuerySerializer, LeaveProductReviewSerializer
from .services import get_product_by_id_or_none, save_product_review, get_all_reviews
from .settings import REVIEW_REWARD


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
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    @check_access_token
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        parameters = dict()
        parameters['is_premium'] = False
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price is not None and min_price.isdigit():
            parameters['price__gte'] = min_price
        if max_price is not None and max_price.isdigit():
            parameters['price__lte'] = max_price
        queryset = Products.objects.filter(**parameters)
        return queryset


class PremiumProductsListAPIView(ListAPIView):
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
        query_serializer=PremiumProductsFiltersSerializer,
        responses={
            status.HTTP_200_OK: ProductSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    @check_access_token
    def get(self, request, *args, **kwargs):
        serializer = PremiumProductsFiltersSerializer(data=request.query_params)
        if serializer.is_valid():
            client_id = serializer.validated_data.get('client_id')
            client = get_client_by_id_or_none(client_id)
            if client is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'client_id': 'Client not found'
                })
            if client.status != ClientsStatuses.PREMIUM.value:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'client_id': 'Client is not premium'
                })
            return super().get(request, *args, **kwargs)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_queryset(self):
        parameters = dict()
        parameters['is_premium'] = True
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price is not None and min_price.isdigit():
            parameters['price__gte'] = min_price
        if max_price is not None and max_price.isdigit():
            parameters['price__lte'] = max_price
        queryset = Products.objects.filter(**parameters)
        return queryset


class ProductsReviewsAPIView(ListAPIView):
    serializer_class = ProductsReviewSerializer

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
        query_serializer=ProductsReviewsQuerySerializer,
        responses={
            status.HTTP_200_OK: 'Review added',
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    @check_access_token
    def get(self, request, *args, **kwargs):
        serializer = ProductsReviewsQuerySerializer(data=request.query_params)
        if serializer.is_valid():
            parameters = dict()
            product_id = serializer.validated_data.get('product_id')
            parameters['product_id'] = product_id
            client_id = serializer.validated_data.get('client_id')
            product = get_product_by_id_or_none(product_id)
            if product is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'product_id': 'Product not found'
                })
            if client_id is not None:
                client = get_client_by_id_or_none(client_id)
                if client is None:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                        'client_id': 'Client not found'
                    })
                parameters['client_id'] = client_id
            reviews = get_all_reviews(**parameters)
            reviews_serializer = ProductsReviewSerializer(reviews, many=True)
            return Response(status=status.HTTP_200_OK, data=reviews_serializer.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LeaveProductReviewAPIView(GenericAPIView):
    serializer_class = LeaveProductReviewSerializer

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
            status.HTTP_200_OK: 'Review leaved',
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    @check_access_token
    def post(self, request):
        serializer = LeaveProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            client_id = serializer.validated_data.get('client_id')
            text = serializer.validated_data.get('text')
            rating = serializer.validated_data.get('rating')
            product = get_product_by_id_or_none(product_id)
            if product is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'product': 'Product not found'
                })
            client = get_client_by_id_or_none(client_id)
            if client is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                    'client': 'Client not found'
                })
            save_product_review(product_id, client_id, text, rating)
            top_up_client_balance(client_id, REVIEW_REWARD)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

