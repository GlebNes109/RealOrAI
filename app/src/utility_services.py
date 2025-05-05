import hashlib
import time
import jwt

from app.src.config import settings


def create_jwt_token(data: dict):
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

def create_hash(password):
    sha256hash = hashlib.sha256()
    sha256hash.update(password.encode('utf-8'))
    return sha256hash.hexdigest()

def calculate_token_TTL():
    TTL = time.time() + 60 * 60 # 1 час
    return TTL