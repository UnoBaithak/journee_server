from fastapi import APIRouter
from users.services import UserService
from users.models.request_models import UserInfoUpdateBody, UserSentiveInfoUpdateBody

router = APIRouter(prefix="/api/user")
user_service = UserService()

@router.get("/{username}")
async def get_user(username: str):
    return user_service.get_user_details(username)

@router.get("/{username}/itineraries")
async def get_user_itineraries(username: str):
    return {"itineraries": user_service.get_user_itineraries(username)}

@router.post("/{user_id}/create_username")
async def update_username(user_id: str, body: dict):
    return user_service.update_username(user_id, body.get("username"))

@router.put("/{username}")
async def update_user_data(user_update_body: UserInfoUpdateBody | UserSentiveInfoUpdateBody):
    # TODO: Implement user update
    pass

@router.get("/")
async def generic_welcome():
    return "On the user route"
