from pydantic import BaseModel
from datetime import datetime

class user(BaseModel):
    email:str
    password:str
    type:str

class createuser(user):
    pass

class userrespon(BaseModel):
    id: int
    email:str
    type:str
    create_at: datetime

    class Config:
        orm_mode = True