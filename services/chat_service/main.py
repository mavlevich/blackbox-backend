from fastapi import FastAPI
from services.chat_service.routers import encryption_router

app = FastAPI(title="Chat Service")

app.include_router(encryption_router.router, prefix="/encryption")
