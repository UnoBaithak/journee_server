import time
from fastapi import HTTPException
import bcrypt
from request_models.auth_request_models import UserAuth
from users.models.user import User
from services.db_service import DBService
from datetime import timedelta
import os
import jwt
from common.decorators import Env

from dotenv import load_dotenv

@Env("auth_service.env")
class AuthService:
    def __init__(self):
        self.user_collection = DBService().get_collection("users")

    def register_user(self, user_data: UserAuth):
        existing_user = self.user_collection.count_documents({"email": user_data.email}) > 0

        if existing_user:
            raise HTTPException(status=400, detail="Email already registered")
        
        new_user = User.create(email=user_data.email, password=self._hash_password(user_data.password))
        result = self.user_collection.insert_one(new_user.model_dump())
        return {"status": "SUCCESS", "id": result.inserted_id}
    
    def login(self, user_data: UserAuth):
        user = self.user_collection.find_one({"email": user_data.email})

        if user is None:
            raise HTTPException(status_code=404, detail="User does not exist")
        
        if not self._passwords_match(user_data.password, user["password"]):
            raise HTTPException(status_code=401, detail = "Invalid email or password")
        
        return {"status": "SUCCESS", "token": self._create_token(user["_id"])}
    
    def _create_token(self, user_id):
        expire = time.time() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
        to_encode = {"user_id": user_id, "exp": expire}
        return jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))

    def _passwords_match(self, user_input: str, stored_password: str):
        return bcrypt.checkpw(user_input.encode("utf-8"), stored_password.encode("utf-8"))

    def _hash_password(self, password: str):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")