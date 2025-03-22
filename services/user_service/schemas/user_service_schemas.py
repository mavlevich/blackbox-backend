from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        orm_mode = True
