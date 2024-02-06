from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str
    password_repeat: str


class UserResponse(UserBase):
    id: int
    username: str
    email: str
    created_at: datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

# Request
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostResponseVote(BaseModel):
    Post: PostResponse
    votes: int
