from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from services.user_service.models.user_service_model import User
from services.user_service.schemas.user_service_schemas import UserCreate
from services.user_service.core.auth_service import hash_password
from typing import Optional


def create_user(user_data: UserCreate, db: Session) -> User:
    existing_user = db.query(User).filter(
        (User.email == user_data.email) |
        (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with given email or username already exists"
        )

    hashed_pw = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pw
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()
