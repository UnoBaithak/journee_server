from pydantic import BaseModel
from typing import Optional

class UserInfoUpdateBody(BaseModel):
    name: Optional[str] = None
    profile_picture: Optional[str] = None

class UserSentiveInfoUpdateBody(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
