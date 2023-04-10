from typing import Callable
from rest_framework.response import Response
from rest_framework import status
from .jwt import JWT
from .exceptions import InvalidAccessTokenException


def check_access_token(func: Callable):

    def wrapper(*args, **kwargs):
        request = args[1]
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        try:
            bearer, token = auth_token.split()  # 'Bearer' {token}
            if bearer != 'Bearer':
                return Response(status=status.HTTP_403_FORBIDDEN)
            jwt = JWT(token)
            check_jwt = JWT(jwt.payload)
            if not check_jwt.is_equal_signature(jwt):
                return Response(status=status.HTTP_403_FORBIDDEN)
            if jwt.is_available():
                return func(*args, **kwargs)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except (InvalidAccessTokenException, ValueError, AttributeError):
            return Response(status=status.HTTP_403_FORBIDDEN)

    return wrapper
