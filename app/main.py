from re import U
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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

@app.post("/singup", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.createuser, db: Session = Depends(get_db)):
    new_user = models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data" : new_user}

@app.get("/user")
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.user).all()
    return {"data": user}

@app.get("/user/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return{"post_detail": user}

@app.put("/Updateuser/{id}", status_code=status.HTTP_201_CREATED)  
def update_post(id: int, update_user: schemas.createuser, db: Session = Depends(get_db)):

    user_query = db.query(models.user).filter(models.user.id == id)

    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    user_query.update(update_user.dict(), synchronize_session=False)

    db.commit()

    return{"data": user_query.first()}

@app.delete("/delete/{id}", status_code=status.HTTP_201_CREATED)
def delete_post(id: int, db: Session = Depends(get_db)):

    user = db.query(models.user).filter(models.user.id == id)

    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    user.delete(synchronize_session=False)

    db.commit()
    return {'message': 'post deleted sussessfully'}


