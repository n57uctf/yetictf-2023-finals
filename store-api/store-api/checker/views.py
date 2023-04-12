from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Products
from .serializers import PutFlagSerializer, PullFlagSerializer


class PutFlagAPIView(GenericAPIView):
    serializer_class = PutFlagSerializer

    def post(self, request):
        serializer = PutFlagSerializer(data=request.data)
        if serializer.is_valid():
            round_number = serializer.validated_data.get('round_number')
            flag = serializer.validated_data.get('flag')
            Products.objects.create(
                name='test',
                description='test description',
                price=100_000,
                is_premium=True,
                extra_info=flag
            )
            return Response(status=status.HTTP_200_OK, data={
                'product created'
            })
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PullFlagAPIView(GenericAPIView):
    serializer_class = PullFlagSerializer

    def get(self, request):
        serializer = PullFlagSerializer(data=request.query_params)
        if serializer.is_valid():
            """
            Make flag unique
            """
            private_info = serializer.validated_data.get('private_info')
            flag = serializer.validated_data.get('flag')
            products = Products.objects.filter(extra_info=flag, price__lte=100_000)
            if not products:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_200_OK, data={
                'flag': products[0].extra_info
            })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class IsAvailableAPIView(APIView):

    def post(self, request):
        return Response(status=status.HTTP_200_OK)
