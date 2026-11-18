"""Password hashing (stdlib PBKDF2) and HTTP Basic authentication."""
import hashlib
import hmac
import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import User

_ITERATIONS = 200_000
basic = HTTPBasic()


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITERATIONS)
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split("$")
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt_hex), _ITERATIONS
    )
    return hmac.compare_digest(digest.hex(), digest_hex)


# Used so a wrong username costs the same time as a wrong password.
_DUMMY_HASH = hash_password(secrets.token_hex(8))


def current_user(
    creds: HTTPBasicCredentials = Depends(basic), db: Session = Depends(get_db)
) -> User:
    user = db.scalar(select(User).where(User.username == creds.username))
    ok = verify_password(creds.password, user.password_hash if user else _DUMMY_HASH)
    if not user or not ok:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
