import hashlib
import time
import jwt

from src.config import settings


def create_jwt_token(data: dict):
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

def create_hash(password):
    sha256hash = hashlib.sha256()
    sha256hash.update(password.encode('utf-8'))
    return sha256hash.hexdigest()

def calculate_token_TTL():
    TTL = time.time() + 60 * 60 # 1 час
    return TTL

'''def get_token(request: Request):
    headers = request.headers
    a = str(headers.get("Authorization"))
    return a[7:]'''

'''def get_user_id(token: str = Depends(get_token)):
    repository = Repository()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")

        if not repository.get_user_by_id(user_id):
            raise jwt.PyJWTError

        return user_id

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован"
        )
        # raise make_http_error(401, "пользователь не авторизован")'''