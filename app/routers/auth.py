# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=23569s
# Authentication
# Session based authentication
#   A session object keeps track if a user is logged in.
#   The session is stored in the backend like a state.
# JWT token authentication
#   Stateless
#   No information is stored at the backend.
#   A JWT token keeps track if a user is logged in.
#   The JWT token is stored at the frontend.
# Authentication flow
#   Client                                             API
#          ------ /login (username + password) ------>
#                                              Verifies the credentials
#                                              Create a JWT token (string)
#                                              secret for the client application
#         <----------------------------- token -------
#         ------ /posts {token} --------------------->
#                                              Verifies the token
#         <------------------------------ data -------
#
# JWT token
#   Header (signing algorithm and token type)
#      {
#        "alg": "HS256",
#        "type": "JWT"
#      }
#   Payload (what ever, not too much, but nothing secret because it's not encrypted)
#      {
#        "sub": "1234567890",
#        "name": "John Doe",
#        "iat": "1516239022"
#      }
#   Verify signature (protection against tempering)
#      HMACSHA256(
#         base64UrlEncode(header) + "." +
#         base64UrlEncode(payload),
#         your-256-bit-api-secret
#      ) secret_base64_encoded
#
# The token is not encrypted. Everybody can read it.
# The token cannot be tempered without knowing the secret.
# The secret is only known by the api server.
# The secret is the critical part for the security.
#
# Login process
#   Client                                         API                                     Database
#          ------ /login (email, password) ------>     ----find the user ---------------->
#                                                      <-----User {(password(hashed)} ----
#                                          Hash the given password and
#                                          compare it to password from
#                                          the database
#         <---------------------------- token ----

# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=24423s

from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm   # requires python-multipart
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(tags=["Authentication"])


# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=24423s
# Login a user
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=25798s
# Use request form by dependency injection to get the user credentials.
# User credentials have to be provided as form data.
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm gives the credentials as username and password..
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=25244s
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer" }

# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=26003s