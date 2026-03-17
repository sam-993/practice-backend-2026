from src.database import SessionLocal
from src.models import User, Court
from src.auth import get_password_hash

def seed_data():
    db = SessionLocal()
    if not db.query(User).filter(User.email == "admin@test.com").first():
        admin = User(
            email="admin@test.com",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            full_name="System Admin"
        )
        db.add(admin)
    
    court = Court(name="Центральный корт", court_type="Теннис", price_per_hour=1500.0)
    db.add(court)
    
    db.commit()
    db.close()
    print("Данные успешно добавлены!")

if __name__ == "__main__":
    seed_data()