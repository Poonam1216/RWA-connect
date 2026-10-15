from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from app.core.config import settings

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)

def create_access_token(user_id: str, society_id: str, roles: list[str]) -> str:
    now = datetime.now(timezone.utc)

    payLoad = {
        "sub" : user_id,
        "society_id" : society_id,
        "roles" : roles,
        "types" : "access",
        "iat" : now,
        "exp" : now + timedelta(minutes=settings.access_token_expire_minutes)
    }

    return jwt.encode(payLoad, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])