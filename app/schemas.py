from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr

from app.database import Base


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True