from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from services.user_service.db.database import get_db
from services.user_service.models.user_service_model import User
from services.user_service.schemas.user_service_schemas import (
    UserCreate,
    UserOut,
    UserLogin,
    UserUpdate,
)
from services.user_service.core.user_service import (
    create_user,
    get_user_by_email,
)
from services.user_service.core.auth_service import (
    verify_password,
    hash_password,
)
from services.user_service.core.jwt_handler import (
    create_access_token,
    get_current_user,
)

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(user_data, db)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # По OAuth2 стандарту, username = email
    user = get_user_by_email(form_data.username, db)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/update", response_model=UserOut)
def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.email:
        user.email = user_update.email
    if user_update.username:
        user.username = user_update.username
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
