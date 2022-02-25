# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=22633s
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=23254s
# Set the common prefix for all routes.
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=23431s
# Set a router tag splitting the swagger documentation into categories.
router = APIRouter(prefix="/posts", tags=["Posts"])


# Get all posts
# Add request parameters to specify the amount of posts,
# to skip posts and to search in the title.
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=31112s
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # Use request parameter to limit the count of posts to select,
    # to skip posts and to search in the title.
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=31112s
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    # Join with votes and group the result by posts to get the number of votes for a post.
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=36926s
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search)).offset(skip).limit(limit)\
        .all()

    # Only fetch the posts of the current user.
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=30468s
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    return posts


# Get a post by its id.
# Define the model used for the response.
@router.get("/{id}", response_model=schemas.PostResponse)
def get_posts(id: int,
              db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", [id])
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # Join with votes and group the result by posts to get the number of votes for a post.
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=37701s
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == id)\
        .first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found.")

    # Don't show posts of other users.from
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=30468s
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action.")

    return post


# Create a new post.
# Define the model used for the response.
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=26879s
# Add oauth2 authentication by dependency injection.
# The type of current_user doesn't really matter.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # # %s is a placeholder for a value. So the values a sanitized
    # # and there is less vulnerability for sql injections.
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # # All changes are state changes and need to be committed to be written to the database.
    # conn.commit()

    # Define a new post.
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # Easier: Convert the post to a dictionary and create the post model by unpacking the dictionary.
    # Add the user who creates the post.
    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=29879s
    new_post = models.Post(owner_id = current_user.id, **post.dict())

    # Add the new post to the database.
    db.add(new_post)
    # Commit the changes.
    db.commit()
    # Reload the creates post from the database to get is with all values.
    db.refresh(new_post)

    return new_post


# Delete a post.
# The default status code has to be set again with the response.
# However, by setting the default status code also here, FastAPI will do some validations,
# e.g. checking, if the response is empty (has to be with code 204).
# Add oauth2 authentication by dependency injection.
# The type of current_user doesn't really matter.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", [id])
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found.")

    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=30061s
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    post_query.delete(synchronize_session=False)
    db.commit()

    # Return an empty response but with the right status code.
    # The default code defines with the path is not used here.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post
# Define the model used for the response.
# Add oauth2 authentication by dependency injection.
# The type of current_user doesn't really matter.
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE ID = %s""",
    #                (post.title, post.content, post.published, id))
    # affected_rows = cursor.rowcount
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found.")

    # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=30061s
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    # post_query.update({"title": post.title, "content": post.content}, synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
