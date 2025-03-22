from pydantic import BaseModel


class EncryptRequest(BaseModel):
    message: str
    password: str


class DecryptRequest(BaseModel):
    encrypted_message: str
    password: str


class EncryptedResponse(BaseModel):
    result: str
