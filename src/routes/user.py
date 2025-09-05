from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserResponse
from src.repositories.user import UserRepository
from src.core.database import get_db
from src.core.auth import get_current_user_id
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    
    existing_user = user_repo.get_user_by_email(str(user_data.email))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )
    
    try:
        new_user = user_repo.create_user(user_data)
        return UserResponse.model_validate(new_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    users = user_repo.get_all_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]
