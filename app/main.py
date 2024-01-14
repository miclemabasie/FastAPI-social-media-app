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

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="miclem", password="1234", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DATABASE CONNECTION WAS SUCCESSFUL")
        break
    except psycopg2.Error as e:
        print("Could not establish a connection to the database")
        print(e)
        time.sleep(3)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/check", status_code=status.HTTP_200_OK)
def index():
    """Checks the heath of the API, if ok, returns OK"""
    return {"message": "OK"}


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    query = db.query(models.Post) # creates the SQL query for getting all the posts from the database
    posts = query.all()
    return {"posts": posts}

@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_detail(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id).first() 
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    return {"data": post}


@app.post("/posts")
def create_post(post: Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)    
    # OR
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # return the new post that was just created
    return {"post": new_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # Try to fetch the post with the given ID from the database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    post_obj = post_query.first()
    return {"data": post_obj}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

