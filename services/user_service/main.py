from fastapi import FastAPI
from services.user_service.db.database import Base, engine
from services.user_service.routers import auth_router, user_router

app = FastAPI(title="User Service")

# Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(user_router.router, prefix="/users", tags=["users"])
