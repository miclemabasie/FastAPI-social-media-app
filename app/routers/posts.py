from fastapi import status, Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from app.schemas import *
from app import models
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)



@router.get("/", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)) -> list[PostResponse]:
    query = db.query(models.Post) # creates the SQL query for getting all the posts from the database
    posts = query.all()
    return posts

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_post_detail(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)) -> PostResponse:
    post = db.query(models.Post).filter(models.Post.id ==id).first() 
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    return post


@router.post("/")
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)) -> PostResponse:
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)    
    # OR
    print(user_id)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # return the new post that was just created
    return new_post


@router.put("/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)) -> PostResponse:
    # Try to fetch the post with the given ID from the database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    post_obj = post_query.first()
    return post_obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


