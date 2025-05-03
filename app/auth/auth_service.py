from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from request_models.auth_request_models import UserAuth
from users.models.user import User
from services.db_service import DBService
from common.decorators import Env
from .oauth_handler import OAuthHandler, OAuthProvider
from .utils import AuthUtils
import logging

logger = logging.getLogger("uvicorn")

@Env("auth_service.env")
class AuthService:
    def __init__(self):
        self.user_collection = DBService().get_collection("users")
        self.oauth_handler = OAuthHandler()

    def register_user(self, user_data: UserAuth):
        existing_user = (
            self.user_collection.count_documents({"email": user_data.email}) > 0
        )

        if existing_user:
            raise HTTPException(status=400, detail="Email already registered")

        new_user = User.create(
            email=user_data.email, password=AuthUtils.hash_password(user_data.password)
        )
        
        new_user_id = self._add_new_user(new_user)
        response = RedirectResponse(url=f"/user/{new_user_id}/create_username", status_code=302)
        
        return response

    def login(self, user_data: UserAuth):
        user = self.user_collection.find_one({"email": user_data.email}, {"_id": 1, "email": 1, "password": 1})

        if user is None:
            raise HTTPException(status_code=404, detail="User does not exist")

        if not AuthUtils.verify_password(user_data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if user.get("username", None) is None:
            response = RedirectResponse(url=f"/user/{str(user["_id"])}/create_username", status_code=302)
            return response

        token = AuthUtils.create_token(str(user["_id"]))
        response = RedirectResponse(url=f"/api/{user.get("username")}/itineraries", status_code=302)
        response.set_cookie("b_token", token, httponly=True, secure=True)
    
        return response

    def handle_oauth(self, request_body: bytes, oauth_provider: OAuthProvider):
        response = self.oauth_handler.process_request_body(request_body, oauth_provider)
        user = self.user_collection.find_one(
            {
                "$or":[
                    {"google_id": response.sub},
                    {"email": response.email}
                ]
            }
        ) 
        if user is None:
            logger.info("New user, create")
            new_user = User.create(
                email=response.email,
                name=response.name,
                google_id=response.sub,
                profile_picture=response.picture,
            )
            new_user_id = self._add_new_user(new_user)
            
            response = RedirectResponse(url=f"http://localhost:3000/auth/create_username", status_code=302)
            return response
        else:
            logger.info("Existing user, update relevant info")
            if user["name"] is None:
                user["name"] = response.name
            
            if user["profile_picture"] is None:
                user["profile_picture"] = response.picture
            
            if user["google_id"] is None:
                user["google_id"] = response.sub
            
            self.user_collection.update_one({"_id": user["_id"]}, {"$set": user})

            redirect_url = f"http://localhost:3000/user/{str(user["username"])}"
            
            token = AuthUtils.create_token(str(user["_id"]))
            response = RedirectResponse(url=redirect_url, status_code=302)
            response.set_cookie("b_token", token, httponly=True, secure=False)
            
            return response

    def update_password_for_user(self, userid: str, password: str):
        hashed_password = AuthUtils.hash_password(password=password)
        self.user_collection.update_one({"_id": userid}, {"$set": {"password": hashed_password}})
        
        response = RedirectResponse(f"/user/{self.user_collection.find_one({"_id": userid}, {"username": 1})["username"]}/itineraries")
        token = AuthUtils.create_token(str(self.user_collection.find_one({"_id": userid}, {"_id": 1})["_id"]))
        response.set_cookie("b_token", token, httponly=True, secure=False)
        return response

    def update_username_for_user(self, userid: str, username: str):
        self.user_collection.update_one({"_id": userid}, {"$set": {"username": username}})
        response = RedirectResponse(url=f"/user/{username}", status_code=302)
        token = AuthUtils.create_token(userid)
        response.set_cookie("b_token", token, httponly=True, secure=False)
        return response

    def _add_new_user(self, new_user: User):
        result = self.user_collection.insert_one(new_user.model_dump())
        return str(result.inserted_id)