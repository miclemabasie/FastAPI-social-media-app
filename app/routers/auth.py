from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserLogin
from app.models import User
from app.utils import verify_password_hash
from app.oauth2 import create_access_token
from app.schemas import Token


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    # Check for password equlity
    if not verify_password_hash(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Create a token

    access_token = create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}