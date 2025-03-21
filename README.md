# Chat Service — Encryption Module

This service is responsible for securely storing and handling encrypted chat messages.

## Encryption System

- AES-256 encryption in CBC mode is used to ensure message confidentiality.
- AES keys are derived from user-provided passwords using PBKDF2 with SHA-256, 100,000 iterations, and a 16-byte random salt.
- Each encrypted message consists of:
  - 16-byte salt,
  - 16-byte IV (initialization vector),
  - AES-encrypted ciphertext.
- The final format stored is a base64-encoded string: `base64(salt + iv + ciphertext)`.
- Decryption fails gracefully when the password is incorrect or the message is corrupted.
- Passwords are never stored or transmitted to the server.

## Test Execution

To run all tests in the project:

```bash
pytest
