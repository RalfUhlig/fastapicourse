from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    # Ensure that email is well-formed by setting the special type.
    email: EmailStr


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# Specific a schema for creating (and updating) a post.
class PostCreate(PostBase):
    pass


# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=20337s

# Specific a schema for post in responses.
class Post(PostBase):
    id: int
    created_at: datetime
    # Add the id of the user who created that post.
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=29620s
    owner_id: int
    # Add the user
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=30817s
    owner: User

    # Pydantic's orm_mode will tell the Pydantic model to read
    # the data even if it is not a dict, but an ORM model
    # (or any other arbitrary object with attributes).
    # This way, instead of only trying to get the id value from
    # a dict, as in id = data['id'], it will also try to get it
    # from an attribute as in id = data.id.
    class Config:
        orm_mode = True


# Schema for posts with votes in responses.
# https://youtu.be/0sOvCWFmrtA?t=37401
class PostResponse(BaseModel):
    Post: Post
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class VoteCreate(BaseModel):
    post_id: int
    # Only accept 0 and 1 for direction.
    # 1 = Create a new vote.
    # 0 = Delete an existing vote.
    dir: conint(ge=0, le=1)
