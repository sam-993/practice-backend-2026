from fastapi import FastAPI
from src.database import engine
from src.courts import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sports Booking API",
    description="API для бронирования спортивных площадок",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Sports Booking API"}