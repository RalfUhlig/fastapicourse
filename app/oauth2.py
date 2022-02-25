# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=25244s
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import schemas, models, database
from .config import settings

# Scheme for oauth2 giving the login endpoint as toke url.
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key for token signature.
SECRET_KEY = settings.secret_key
# Algorithm for token signature.
ALGORITHM = settings.signing_algorithm
# Time in minutes after that the token expire.
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


# Get the current user.
# Fetch the user data from the database.
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=27493s
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    # Fetch the user from the database.
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
