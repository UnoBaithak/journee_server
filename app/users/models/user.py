from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    """User Database Model"""
    email: str
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    google_id: Optional[str] = None
    profile_picture: Optional[str] = None
    last_login: Optional[datetime] = None
    conversations: List[str] = []
    itineraries: dict = {
        "bookmarked": [],
        "future": [],
        "completed": [],
        "draft": []
    }

    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return None
        
        data = data.copy()
        if "_id" in data:
            del data["_id"]
        
        return cls(**data)
    
    def dao(self):
        return {
            "email": self.email,
            "name": self.name,
            "profilePicture": self.profile_picture,
            "username": self.username
        }

    # TODO: might not be needed as default initializations are done by pydantic which are same. 
    @staticmethod
    def create(
        email: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        google_id: Optional[str] = None,
        profile_picture: Optional[str] = None,
        last_login: Optional[datetime] = None,
        conversations: Optional[List[str]] = None,
        itineraries: Optional[dict] = None
    ):
        return User(
            email=email,
            username=username,
            name=name,
            password=password,
            google_id=google_id,
            profile_picture=profile_picture,
            last_login=last_login or datetime.utcnow(),
            conversations=conversations or [],
            itineraries=itineraries or {
                "bookmarked": [],
                "future": [],
                "completed": [],
                "draft": []
            }
        )