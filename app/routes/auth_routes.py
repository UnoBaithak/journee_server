from fastapi import APIRouter, Request
from auth import AuthService
from request_models.auth_request_models import UserAuth
from auth.oauth_handler import OAuthProvider
from urllib.parse import parse_qs

router = APIRouter(prefix="/api/auth")
auth_service = AuthService()

@router.post("/register")
async def register_user(user_data: UserAuth, request: Request):
    return auth_service.register_user(user_data, request.base_url)

@router.post("/login")
async def login(user_data: UserAuth, request: Request):
    return auth_service.login(user_data, request.base_url)

@router.post("/create_username")
async def update_username_for_user(body: dict, request: Request):
    return auth_service.update_username_for_user(body.get("userid"), body.get("password"), request.base_url)

@router.post("/{userid}/create_password")
async def update_password_for_user(userid: str, body: dict, request: Request):
    return auth_service.update_password_for_user(userid, body.get("password"), request.base_url)

@router.post("/google-callback")
async def handle_google_callback(request: Request):
    body = await request.body()
    return auth_service.handle_oauth(body, OAuthProvider.GOOGLE, request.base_url)

@router.get("/")
async def generic_welcome():
    return "On the auth route"