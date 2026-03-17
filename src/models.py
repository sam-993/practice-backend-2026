from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="user")
    bookings = relationship("Booking", back_populates="owner")

class Court(Base):
    __tablename__ = "courts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    court_type = Column(String, nullable=False) # Теннис, футбол и т.д.
    description = Column(String)
    price_per_hour = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

    bookings = relationship("Booking", back_populates="court")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    court_id = Column(Integer, ForeignKey("courts.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="confirmed") 

    owner = relationship("User", back_populates="bookings")
    court = relationship("Court", back_populates="bookings")