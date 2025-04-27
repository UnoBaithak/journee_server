from fastapi import APIRouter
from users.user_service import UserService

router = APIRouter(prefix="/api/user")
user_service = UserService()

@router.get("/{user_id}")
async def get_user(user_id: str):
    return user_service.get_user_details(user_id)

@router.post("/{user_id}/itineraries")
async def get_user_itineraries(user_id: str):
    return {"itineraries": user_service.get_user_itineraries(user_id)}

@router.get("/")
async def generic_welcome():
    return "On the user route"
