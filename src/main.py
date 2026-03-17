from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.database import engine, get_db
from src import models, schemas, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sports Booking API")


@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email, 
        hashed_password=hashed_pwd, 
        full_name=user.full_name,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/courts", response_model=list[schemas.CourtOut])
def list_courts(db: Session = Depends(get_db)):
    return db.query(models.Court).all()

@app.post("/courts", response_model=schemas.CourtOut)
def create_court(
    court: schemas.CourtCreate, 
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.check_admin) 
):
    new_court = models.Court(**court.model_dump())
    db.add(new_court)
    db.commit()
    db.refresh(new_court)
    return new_court

@app.put("/courts/{court_id}", response_model=schemas.CourtOut)
def update_court(
    court_id: int, 
    court_data: schemas.CourtUpdate, 
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.check_admin)
):
    db_court = db.query(models.Court).filter(models.Court.id == court_id).first()
    if not db_court:
        raise HTTPException(status_code=404, detail="Court not found")
    
    for key, value in court_data.model_dump(exclude_unset=True).items():
        setattr(db_court, key, value)
    
    db.commit()
    db.refresh(db_court)
    return db_court

@app.delete("/courts/{court_id}")
def delete_court(
    court_id: int, 
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.check_admin)
):
    db_court = db.query(models.Court).filter(models.Court.id == court_id).first()
    if not db_court:
        raise HTTPException(status_code=404, detail="Court not found")
    db.delete(db_court)
    db.commit()
    return {"message": "Court deleted successfully"}