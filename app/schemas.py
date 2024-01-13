from pydantic import BaseModel

class PostBase(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: str


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    pass