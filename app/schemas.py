from pydantic import BaseModel
from datetime import datetime


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


class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str
    password_repeat: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

