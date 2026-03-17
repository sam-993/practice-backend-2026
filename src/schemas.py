from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class CourtBase(BaseModel):
    name: str
    court_type: str
    description: Optional[str] = None
    price_per_hour: float
    is_active: bool = True

class CourtCreate(CourtBase):
    pass

class CourtUpdate(CourtBase):
    name: Optional[str] = None
    court_type: Optional[str] = None
    price_per_hour: Optional[float] = None

class CourtOut(CourtBase):
    id: int
    class Config:
        from_attributes = True