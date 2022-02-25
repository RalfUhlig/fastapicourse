# Database models
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

# All models have to be derived from Base
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(String(10000), nullable=False)
    # A default values definition for the column has to be done with server_default.
    # default only sets a default value for the model.
    published = Column(Boolean, server_default="1", nullable=False)
    # The default aof TIMESTAMP is current_timestamp() ON UPDATE current_timestamp().
    # So the column value will be changed on every update. To set a default value only
    # on insert, it has to be set explicitly.
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    # Create a reference to a user with a foreign key.
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=29240s
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Set a relationship between users and posts, so that the user's email
    # can be fetched with a post. The relationship is accordingly to the foreign key.
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=30817s
    owner = relationship("User")


# Table for users.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


# Table for votes
class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
