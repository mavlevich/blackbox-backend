from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64, os


def generate_key(password: str, salt: bytes) -> bytes:
    """
    Generates AES key from password using PBKDF2 + SHA256.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_message(message: str, password: str) -> str:
    """
    Encrypts message using AES-256-CBC with key derived from password.
    Returns base64(salt + iv + ciphertext)
    """
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = generate_key(password, salt)

    padder = padding.PKCS7(128).padder()
    padded = padder.update(message.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    return base64.b64encode(salt + iv + ciphertext).decode()


def decrypt_message(encrypted: str, password: str) -> str:
    """
    Decrypts base64-encoded (salt + iv + ciphertext) message.
    Returns original text or an error string.
    """
    try:
        decoded = base64.b64decode(encrypted)
        salt, iv, ct = decoded[:16], decoded[16:32], decoded[32:]
        key = generate_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ct) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        text = unpadder.update(padded) + unpadder.finalize()
        return text.decode()

    except Exception:
        return "Decryption failed: incorrect password or corrupted message"

