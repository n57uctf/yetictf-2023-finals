import random
import string
import io
import hashlib
import jwt


def get_auth_token(login: str):
    return jwt.encode({"login": login}, "9a9e68aafc2f893efe9d4f4dfe94360d", algorithm="HS256")


def verify_auth_token(token: str):
    return jwt.decode(token, "9a9e68aafc2f893efe9d4f4dfe94360d", algorithms=["HS256"])["login"]


def hash_sha256(data: str):
    return hashlib.sha256(data.encode()).hexdigest()


def verify_hash(hash_string: str, data: str):
    return hashlib.sha256(data.encode()).hexdigest() == hash_string


def isBool(isVip: str):
    return isVip in ['true', '1']