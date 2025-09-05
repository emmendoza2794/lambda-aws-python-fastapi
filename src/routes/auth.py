from fastapi import APIRouter, HTTPException, status, Depends, Form
from sqlalchemy.orm import Session
from src.schemas.user import LoginResponse, UserResponse
from src.repositories.user import UserRepository
from src.core.database import get_db
from src.core.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    
    user = user_repo.authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"user_id": user.id})
    
    return LoginResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )
