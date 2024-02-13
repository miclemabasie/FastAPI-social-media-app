from jose import JWTError, jwt
import time
from datetime import timedelta, datetime
from app.schemas import TokenData
from fastapi import Depends, status, HTTPException

from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv
import os




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "9ab1197da051af6fb51923c545ff631357d08f15bca2366ed974d83881d7c41e"
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verirfy_access_token(token: int, credentials_exception):
    print("verifying password #########")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
        id: int = payload.get("user_id")
    
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verirfy_access_token(token, credentials_exception)

