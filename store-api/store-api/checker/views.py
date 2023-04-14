import json
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Products
from clients.models import Clients
from clients.registration.services import make_sha256_hash
from .serializers import PutFlagSerializer, PullFlagSerializer
from .services import get_random_product_info

import logging


class PutFlagAPIView(GenericAPIView):
    serializer_class = PutFlagSerializer

    def post(self, request):
        serializer = PutFlagSerializer(data=request.data)
        if serializer.is_valid():
            round_number = serializer.validated_data.get('round_number')
            flag = serializer.validated_data.get('flag')
            extra_info = f'{round_number} {flag}'
            name, desc, price = get_random_product_info()
            Products.objects.create(
                name=name,
                description=desc,
                price=price,
                is_premium=True,
                extra_info=extra_info
            )
            return Response(status=status.HTTP_200_OK, data={
                'product created'
            })
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PullFlagAPIView(GenericAPIView):
    serializer_class = PullFlagSerializer

    def post(self, request):
        serializer = PullFlagSerializer(data=request.data)
        if serializer.is_valid():
            private_info = serializer.validated_data.get('private_info')
            dict_private_info = json.loads(private_info)
            try:
                Clients.objects.get(
                    email=dict_private_info.get('email'),
                    password=make_sha256_hash(dict_private_info.get('password'))
                )
                round_number = dict_private_info.get('round_number')
                flag = serializer.validated_data.get('flag')
                extra_info = f'{round_number} {flag}'
                product = Products.objects.filter(
                    extra_info=extra_info,
                    price__lte=1_000_000
                ).first()
                if not product:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                return Response(status=status.HTTP_200_OK, data={
                    'flag': product.extra_info.split()[1],
                })
            except Clients.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class IsAvailableAPIView(APIView):

    def post(self, request):
        return Response(status=status.HTTP_200_OK)
