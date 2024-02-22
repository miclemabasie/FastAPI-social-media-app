from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.schemas import *
from app import models
from app.database import get_db
from app.validators import validate_user_email
from app.utils import custom_password_hash

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    users = db.query(models.User)
    users = users.all()
    return users



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    # extract the fields from the request body
    # Check if password match
    email, username, password, password_re = user.model_dump().values()
    if password != password_re:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    if not validate_user_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email ID")
    hashed_password = custom_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, password=hashed_password)

    # Check if user exist in the database
    user_check = db.query(models.Post).filter(models.User.email == user.email).first()
    if user_check is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with Email ID already exists")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)) -> UserResponse:

    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id does not exist")
    return user

