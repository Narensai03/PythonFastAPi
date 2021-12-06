from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class user(BaseModel):
    email:EmailStr
    password:str
    type:str

class createuser(user):
    pass

class userrespon(BaseModel):
    id: int
    email:EmailStr
    type:str
    create_at: datetime

    class Config:
        orm_mode = True

class userlogin(BaseModel):
    email: EmailStr
    password: str
    type:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
