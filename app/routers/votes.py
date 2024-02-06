from fastapi import status, Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from app.schemas import *
from app import models
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/votes",
    tags = ["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):

    # get the post
    post = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user_id.id)
    found = vote_query.first()
    if vote.dir == 1:
        if found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Can't like the same post twice")
        new_vote = models.Vote(post_id = vote.post_id, user_id = user_id.id)
        db.add(new_vote)
        db.commit()

    else:
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}