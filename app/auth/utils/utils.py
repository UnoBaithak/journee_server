import os
import time
from datetime import timedelta
import bcrypt
from fastapi import Request
import jwt
from common.decorators import Env
from jwt import ExpiredSignatureError, InvalidTokenError

@Env("auth_service.env")
class AuthUtils:
    @staticmethod
    def create_token(user_id):
        expire = time.time() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))).total_seconds()
        to_encode = {"user_id": user_id, "exp": expire}
        
        return jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))
    
    @staticmethod
    def verify_password(user_input: str, stored_password: str):
        return bcrypt.checkpw(user_input.encode("utf-8"), stored_password.encode("utf-8"))

    @staticmethod
    def hash_password(password: str):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    @staticmethod
    def decode_jwt_token(request: Request):
        token = request.cookies.get("b_token")
        if not token:
            payload = {
                "user_id": None
            }
            return payload
        try:
            payload = jwt.decode(
                token,
                os.getenv("JWT_SECRET_KEY"),
                algorithms=[os.getenv("JWT_ALGORITHM")]
            )
            return payload
        except ExpiredSignatureError:
            raise Exception("Token has expired")
        except InvalidTokenError:
            raise Exception("Invalid token")