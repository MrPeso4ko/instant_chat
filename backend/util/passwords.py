import os
from hashlib import scrypt

from config import get_settings

settings = get_settings()


def _hash(password: str, salt: bytes) -> bytes:
    return scrypt(password.encode("utf-8"), salt=salt, n=settings.hash.n, r=settings.hash.r, p=settings.hash.p)


def hash_password(password: str) -> (bytes, bytes):
    salt = os.urandom(16)
    hashed_password = _hash(password, salt)
    return hashed_password, salt


def check_password(password: str, hashed_password: bytes, salt: bytes) -> bool:
    return _hash(password, salt) == hashed_password
