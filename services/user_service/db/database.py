from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from services.user_service.db.config import Settings
from sqlalchemy.orm import Session
from contextlib import contextmanager

settings = Settings()

DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
