from fastapi import FastAPI
from services.user_service.db.database import Base, engine


app = FastAPI(title="User Service")

Base.metadata.create_all(bind=engine)
