"""
This module contains additional functions for secretkeys app
"""
from __future__ import annotations
import base64
import hashlib
from random import choice
from string import digits, ascii_letters, punctuation
from .models import SecretKeys


def save_secret_key(key: str, product_id: int) -> SecretKeys:
    """Save secret key to `SecretKeys` model
    :param key: encoded string
    :type key: str
    :param product_id: id of the product that will be use this key to decode description
    :type product_id: int
    :raise IntegrityError: raises if record for product already exists
    :raise ValueError: raises if `generate_key` param is False and key is not specified
    :returns: instance of `SecretKeys` model
    :rtype: SecretKeys
    """
    if not isinstance(key, str):
        raise ValueError('Key is not specified or type is not str')
    return SecretKeys.objects.create(
        key=key,
        product_id=product_id
    )


def get_secret_key_by_product_id_or_none(product_id: int) -> SecretKeys | None:
    """Save secret key to `SecretKeys` model
    :param product_id: id of the product
    :type product_id: int
    :returns: instance of `SecretKeys` model if exists or None instead
    :rtype: SecretKeys or None
    """
    return SecretKeys.objects.filter(product_id=product_id).first()


def encode_string(string: str, secret_key: str) -> str:
    """Encodes the string using secret key
    :param string: string to encode
    :type string: str
    :param secret_key: key that will be used to encode the string
    :type secret_key: str
    :return: encoded string
    :rtype: str
    """
    sha256 = hashlib.sha256()
    sha256.update(secret_key.encode())
    encoded_key = sha256.digest()
    encoded_bytes = string.encode()
    encoded = bytearray()
    for i in range(len(encoded_bytes)):
        key_index = i % len(encoded_key)
        encoded.append(encoded_bytes[i] ^ encoded_key[key_index])
    return base64.b64encode(bytes(encoded)).decode()


def decode_string(string: str, secret_key: str) -> str:
    """Decodes the string using secret key
    :param string: string to decode
    :type string: str
    :param secret_key: key that will be used to decode the string
    :type secret_key: str
    :return: decoded string
    :rtype: str
    """
    sha256 = hashlib.sha256()
    sha256.update(secret_key.encode())
    encoded_key = sha256.digest()
    decoded_bytes = bytearray(base64.b64decode(string))
    decoded = ''
    for i in range(len(decoded_bytes)):
        key_index = i % len(encoded_key)
        decoded += chr(decoded_bytes[i] ^ encoded_key[key_index])
    return decoded


def generate_random_string(length: int = 30) -> str:
    """Generates 30 character string of random characters (string.printable)
    :param length: length of the final string, default = 30
    :type length: int
    :return: string
    :rtype: str
    """
    symbols = digits + ascii_letters + punctuation
    string = ''
    for _ in range(length):
        string += choice(symbols)
    return string


