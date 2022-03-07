from typing import Optional
from pydantic import BaseModel, PositiveInt, EmailStr, conint
from datetime import datetime

#We create a class that is the template for our posts, what the user should input
#  this is a pydantic model
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime

    class Config:
        orm_mode=True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True    

#Extend PostBase
class PostCreate(PostBase):
    pass

#Handle what we send to the user
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    
    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_model=True

class UserLogin (BaseModel):
        email : EmailStr
        password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional [str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint (le=1)

