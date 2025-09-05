from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.models.user import User
from src.schemas.user import UserCreate
from src.core.auth import hash_password, verify_password
from typing import Optional
import uuid


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = hash_password(user_data.password)
        
        db_user = User(
            id=uuid.uuid4(),
            name=user_data.name,
            email=str(user_data.email),
            phone=user_data.phone,
            password=hashed_password
        )
        
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Email already exists")
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if user and verify_password(password, user.password):
            return user
        return None