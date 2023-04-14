from __future__ import annotations
import string
import random
import hmac
from typing import Tuple, Dict
from datetime import datetime, timedelta, timezone
from json import dumps, loads
from hashlib import sha256
from base64 import urlsafe_b64encode, urlsafe_b64decode
from store.settings import env
from .exceptions import InvalidAccessTokenException


JWT_DEFAULT_HEADER = {"alg": "HS256", "typ": "JWT"}
ACCESS_TOKEN_DEFAULT_LIFETIME_IN_MINUTES = 90
REFRESH_TOKEN_DEFAULT_LIFETIME_IN_MINUTES = 43800  # 1 month


def get_token_expiration_time_in_utc(token_lifetime_in_minutes: int) -> int:
    """ Calculate token lifetime from current time in utc
    :param token_lifetime_in_minutes: token lifetime in minutes
    :type token_lifetime_in_minutes: int
    :return: token expiration time
    :rtype: int
    """
    utc_datetime = datetime.now(timezone.utc)
    expiration_time = utc_datetime + timedelta(minutes=token_lifetime_in_minutes)
    return int(expiration_time.timestamp())


class JWT:
    """
    This class create JWT tokens.
    If you pass a dict as parameter it will create a pair of access and refresh tokens,
        and it will use the dict as payload.
    If you pass a string as a parameter, it will try to decode the data and also create
        a pair of access and refresh tokens with payload that was encoded in the string parameter

    :param payload: payload
    :type payload: dict or str
    """

    def __init__(self, payload: dict | str):
        if not isinstance(payload, dict) and not isinstance(payload, str):
            raise TypeError()
        self._access_token = None
        self._refresh_token = None
        if isinstance(payload, str):
            try:
                self._header = None
                self._payload = None
                self._signature = ''
                self._decode_parameters_from_string(payload)
                return
            except:
                raise InvalidAccessTokenException()
        self._header = JWT_DEFAULT_HEADER
        self._payload = payload
        if self._payload.get('exp') is None:
            self._payload['exp'] = get_token_expiration_time_in_utc(ACCESS_TOKEN_DEFAULT_LIFETIME_IN_MINUTES)
        self._signature = self._create_signature()

    def time_to_left(self) -> int:
        expiration_time = self._payload.get('exp')
        current_time = datetime.now(timezone.utc).timestamp()
        return expiration_time - current_time

    def is_available(self) -> bool:
        """Check is access_token is still available
        :return: True if available else False
        :rtype: bool
        """
        return self.time_to_left() > 0

    def is_equal_signature(self, other: JWT) -> bool:
        return self._signature == other._signature

    def as_dict(self) -> Dict[str, str]:
        """
        Returns dict with refresh and access tokens, for example:
        {
            'access_token': 'access_token_here',
            'refresh_token': 'refresh_token_here'
        }
        :return: dict with refresh and access tokens
        :rtype: Dict[str, str]
        """
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token
        }

    @property
    def access_token(self) -> str:
        if self._access_token is None:
            self._access_token = self._create_access_token()
        return self._access_token

    @property
    def refresh_token(self) -> str:
        if self._refresh_token is None:
            self._refresh_token = self._create_refresh_token()
        return self._refresh_token

    @property
    def payload(self) -> dict:
        return self._payload

    def _decode_parameters_from_string(self, data: str) -> None:
        header, payload, signature = data.split('.')
        decoded_header = self._base64_url_decode(header)
        decoded_payload = self._base64_url_decode(payload)
        self._payload = loads(decoded_payload)
        self._signature = signature

    def _create_access_token(self) -> str:
        encoded_header, encoded_payload = self._encode_header_and_payload()
        return f'{encoded_header}.' \
               f'{encoded_payload}.' \
               f'{self._signature}'

    def _create_refresh_token(self) -> str:
        random_string = self._generate_random_string()
        exp_time = get_token_expiration_time_in_utc(REFRESH_TOKEN_DEFAULT_LIFETIME_IN_MINUTES)
        payload = {
            'is_valid': True,
            'exp': exp_time
        }
        str_payload = self._dict_to_str(payload)
        random_string = self._base64_url_encode(random_string)
        str_payload = self._base64_url_encode(str_payload)
        refresh_token = f'{random_string}.{str_payload}.'
        access_token = self._create_access_token()
        refresh_token += access_token[len(access_token) - 10: len(access_token)]
        return refresh_token

    def _dict_to_str(self, dictionary: dict) -> str:
        return dumps(dictionary)

    def _create_signature(self) -> str:
        secret_key = env.str('JWT_SECRET_KEY')
        encoded_header, encoded_payload = self._encode_header_and_payload()
        data = f'{encoded_header}.{encoded_payload}'
        signature = hmac.new(bytes(secret_key, 'utf-8'),
                             msg=bytes(data, 'utf-8'),
                             digestmod=sha256).hexdigest()
        return signature

    def _encode_header_and_payload(self) -> Tuple[str, str]:
        str_header = self._dict_to_str(self._header)
        str_payload = self._dict_to_str(self._payload)

        encoded_header = self._base64_url_encode(str_header)
        encoded_payload = self._base64_url_encode(str_payload)

        return encoded_header, encoded_payload

    def _generate_random_string(self, string_length: int = 20) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(random.choice(alphabet) for _ in range(string_length))

    def _base64_url_encode(self, data: str) -> str:
        d = data.encode('utf-8')
        return urlsafe_b64encode(d).rstrip(b'=').decode('utf-8')

    def _base64_url_decode(self, data: str) -> str:
        padding = b'=' * (4 - (len(data) % 4))
        d = data.encode('utf-8')
        return urlsafe_b64decode(d + padding).decode('utf-8')



