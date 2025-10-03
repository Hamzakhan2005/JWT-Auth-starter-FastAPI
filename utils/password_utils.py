from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt (truncate to 72 chars)"""
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash (truncate to 72 chars)"""
    return pwd_context.verify(plain_password[:72], hashed_password)
