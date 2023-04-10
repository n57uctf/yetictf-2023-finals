from hashlib import sha256


def make_sha256_hash(string: str) -> str:
    return sha256(string.encode('utf-8')).hexdigest()

