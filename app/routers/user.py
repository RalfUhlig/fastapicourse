# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=22633s
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=23254s
# Set the common prefix for all routes.
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=23431s
# Set a router tag splitting the swagger documentation into categories.
router = APIRouter(prefix="/users", tags=["Users"])

# Create a new user.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password.
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get a user by its id.
# Fetch also the user from the database here.
@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found.")

    return user
