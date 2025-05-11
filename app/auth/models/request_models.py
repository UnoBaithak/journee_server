from pydantic import BaseModel
from typing import Optional

class UserAuth(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

class GoogleIDResponse(BaseModel):
    iss: str  # Issuer
    nbf: Optional[int] = None  # Not Before (optional, sometimes missing)
    aud: str  # Audience (your client ID)
    sub: str  # Subject (user's unique Google Account ID)
    hd: Optional[str] = None  # Hosted domain (optional)
    email: Optional[str] = None  # User's email (optional)
    email_verified: Optional[bool] = None  # Email verified (optional)
    azp: Optional[str] = None  # Authorized party (optional)
    name: Optional[str] = None  # User's name (optional)
    picture: Optional[str] = None  # URL to user's profile picture (optional)
    given_name: Optional[str] = None  # Given name (optional)
    family_name: Optional[str] = None  # Family name (optional)
    iat: int  # Issued At (Unix timestamp)
    exp: int  # Expiration time (Unix timestamp)
    jti: Optional[str] = None  # JWT ID (optional)
