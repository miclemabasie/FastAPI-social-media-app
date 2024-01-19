from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# Databases
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schemas import PostCreate, PostUpdate, PostResponse, UserResponse, UserCreate, Token
from .validators import validate_user_email
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm




pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

models.Base.metadata.create_all(bind=engine)


app = FastAPI()





@app.get("/check", status_code=status.HTTP_200_OK)
def index():
    """Checks the heath of the API, if ok, returns OK"""
    return {"message": "OK"}


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)) -> list[PostResponse]:
    query = db.query(models.Post) # creates the SQL query for getting all the posts from the database
    posts = query.all()
    return posts

@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_detail(id: int, db: Session = Depends(get_db)) -> PostResponse:
    post = db.query(models.Post).filter(models.Post.id ==id).first() 
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    return post


@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)    
    # OR
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # return the new post that was just created
    return new_post


@app.put("/posts/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    # Try to fetch the post with the given ID from the database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    post_obj = post_query.first()
    return post_obj

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# users

@app.get("/users")
def get_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    users = db.query(models.User)
    users = users.all()
    return users



@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    # extract the fields from the request body
    # Check if password match
    email, username, password, password_re = user.model_dump().values()
    if password != password_re:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    if not validate_user_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email ID")
    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(username=user.username, email=user.email, password=hashed_password)

    # Check if user exist in the database
    user_check = db.query(models.Post).filter(models.User.email == user.email).first()
    if user_check is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with Email ID already exists")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user





if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

