# Chat Service — Encryption Module

This service is responsible for securely storing and handling encrypted chat messages.

---

## ⚖️ Encryption System

- AES-256 encryption in CBC mode is used to ensure message confidentiality.
- AES keys are derived from user-provided passwords using PBKDF2 with SHA-256,
  100,000 iterations, and a 16-byte random salt.
- Each encrypted message consists of:
  - 16-byte salt,
  - 16-byte IV (initialization vector),
  - AES-encrypted ciphertext.
- The final format stored is a base64-encoded string:
  `base64(salt + iv + ciphertext)`.
- Decryption fails gracefully when the password is incorrect or the message is corrupted.
- Passwords are never stored or transmitted to the server.

---

## 📚 Local Development Setup

### 1. PostgreSQL Configuration

Make sure PostgreSQL is installed and running locally. Then execute:

```bash
psql -U postgres
```

Inside the prompt:

```sql
CREATE DATABASE blackbox_users;
CREATE USER blackbox_user WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE blackbox_users TO blackbox_user;
```

### 2. Environment Variables

Create a `.env` file in the project root:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=blackbox_users
DB_USER=blackbox_user
DB_PASSWORD=1234
```

Or copy from example:

```bash
cp .env.example .env
```

And ensure `.env` is in `.gitignore`:

```bash
echo ".env" >> .gitignore
```

---

## 📆 Migrations

To generate and apply database migrations:

```bash
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

---

## 🔧 Test Execution

To run all tests in the project:

```bash
pytest
```

To run tests for a specific microservice:

```bash
pytest services/chat_service
```

---

## 📁 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

If regenerating:

```bash
pip freeze > requirements.txt
```

Required packages include:
- `alembic`
- `pydantic-settings`
- `psycopg2-binary`
- `python-dotenv`
- `cryptography`

---

## ⚡ Example Requests (via Postman/cURL)

Coming soon after endpoint implementation.

---
