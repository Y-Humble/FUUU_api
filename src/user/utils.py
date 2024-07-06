import bcrypt


def hash_password(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)
