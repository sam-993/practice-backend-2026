from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ReviewCreate(BaseModel):
    court_id: int
    rating: int
    comment: str

class ReviewOut(ReviewCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class CourtOut(CourtBase):
    id: int
    avg_rating: Optional[float] = 0.0 
    class Config:
        from_attributes = True
class BookingBase(BaseModel):
    court_id: int
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    user_id: int
    status: str
    class Config:
        from_attributes = True

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