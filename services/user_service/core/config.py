from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    jwt_secret: str = Field(..., env="JWT_SECRET")
    db_host: str = Field(..., env="DB_HOST")
    db_port: str = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
