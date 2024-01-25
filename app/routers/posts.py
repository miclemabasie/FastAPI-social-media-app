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
    query = db.query(models.Post).filter(models.Post.owner_id == user_id.id) # creates the SQL query for getting all the posts from the database
    posts = query.all()
    return posts

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_post_detail(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)) -> PostResponse:
    post = db.query(models.Post).filter(models.Post.id ==id).first() 
    if post is None:
        print("Post not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    return post


@router.post("/")
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)) -> PostResponse:
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)    
    # OR
    print(user_id)
    print("This is the new post: ##########: ", user_id.id)
    new_post = models.Post(**post.model_dump(), owner_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # return the new post that was just created
    return new_post


@router.put("/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)) -> PostResponse:
    # Try to fetch the post with the given ID from the database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_object = post_query.first()
    if post_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    if post_object.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    post_query.update(post.model_dump(), synchronize_session=False)
    print("user credentials: ", user_id.id, post_object.owner_id)
    db.commit()
    return post_object

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    if post.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    post.delete(synchronize_session=False)
    
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


