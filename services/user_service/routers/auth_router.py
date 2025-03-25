from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from services.user_service.db.database import get_db
from services.user_service.schemas.user_service_schemas import UserCreate, UserOut
from services.user_service.services.user_service import create_user, get_user_by_email
from services.user_service.services.auth_service import verify_password
from services.user_service.services.jwt_handler import create_access_token
from services.user_service.services.auth_service import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(user_data, db)


@router.post("/login")
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(user_data.email, db)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def get_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
