from fastapi import APIRouter
from auth import AuthService
from request_models.auth_request_models import UserAuth

router = APIRouter(prefix="/api/auth")
auth_service = AuthService()

@router.post("/register")
async def register_user(user_data: UserAuth):
    return auth_service.register_user(user_data)

@router.post("/login")
async def login(user_data: UserAuth):
    return auth_service.login(user_data)

@router.get("/")
async def generic_welcome():
    return "On the auth route"