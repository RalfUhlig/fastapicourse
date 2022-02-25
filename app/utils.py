# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=21807s
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=22129s
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash a password.
def hash(password: str):
    return pwd_context.hash(password)


# Verify a password.
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
