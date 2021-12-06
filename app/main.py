from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:

    try:
        conn = psycopg2.connect(host= 'localhost', database ='fastapi', user= 'postgres', 
    password= 'Nissi123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfully")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error: ", error)
        time.sleep(2)

my_user = [{"email": "Naren@gmail.com", "password": "naren", "id": 1}, 
        {"email": "Naren@gmail.com", "password": "naren", "id": 2}]

def find_user(id):
    for p in my_user:
        if p["id"] == id:
            return p
 
def find_index_user(id):
    for i, p in enumerate(my_user):
        if p['id'] == id:
            return i 

app.include_router(user.router)
app.include_router(auth.router)
