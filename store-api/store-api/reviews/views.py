from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from clients.services import get_client_by_id_or_none, top_up_client_balance
from tokens.decorators import check_access_token
from .serializers import ReviewsQuerySerializer, ReviewSerializer, LeaveReviewSerializer
from products.services import get_product_by_id_or_none
from .services import save_review, get_all_reviews
from .settings import REVIEW_REWARD


class ReviewsAPIView(ListAPIView):
    serializer_class = ReviewSerializer

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
        query_serializer=ReviewsQuerySerializer,
        responses={
            status.HTTP_200_OK: 'Review added',
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    @check_access_token
    def get(self, request, *args, **kwargs):
        serializer = ReviewsQuerySerializer(data=request.query_params)
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
            reviews_serializer = ReviewSerializer(reviews, many=True)
            return Response(status=status.HTTP_200_OK, data=reviews_serializer.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LeaveReviewAPIView(GenericAPIView):
    serializer_class = LeaveReviewSerializer

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
        serializer = LeaveReviewSerializer(data=request.data)
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
            save_review(product_id, client_id, text, rating)
            top_up_client_balance(client_id, REVIEW_REWARD)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


