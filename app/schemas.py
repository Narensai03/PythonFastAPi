from pydantic import BaseModel

class user(BaseModel):
    email:str
    password:str
    type:str

class createuser(user):
    pass
