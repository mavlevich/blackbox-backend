from fastapi import APIRouter
from services.chat_service.schemas.encryption_schemas import (
    EncryptRequest, DecryptRequest, EncryptedResponse
)
from services.chat_service.services.encryption import (
    encrypt_message, decrypt_message
)

router = APIRouter()


@router.post("/encrypt", response_model=EncryptedResponse, tags=["Encryption"])
def encrypt(req: EncryptRequest):
    encrypted = encrypt_message(req.message, req.password)
    return EncryptedResponse(result=encrypted)


@router.post("/decrypt", response_model=EncryptedResponse, tags=["Encryption"])
def decrypt(req: DecryptRequest):
    decrypted = decrypt_message(req.encrypted_message, req.password)
    return EncryptedResponse(result=decrypted)
