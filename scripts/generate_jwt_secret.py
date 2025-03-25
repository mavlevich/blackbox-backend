import secrets


def generate_jwt_secret():
    secret = secrets.token_hex(32)
    print(f"Generated JWT_SECRET:\n{secret}")


if __name__ == "__main__":
    generate_jwt_secret()
