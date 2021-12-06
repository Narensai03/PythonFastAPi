from sys import prefix
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter()

@router.post("/newuser", status_code=status.HTTP_201_CREATED, response_model=schemas.userrespon)
def create_user(user: schemas.createuser, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    return new_user

@router.get("/getuser", response_model=List[schemas.userrespon])
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.user).all()
    return user

@router.get("/user/{id}", response_model=schemas.userrespon)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User does not exist")
    return user

@router.put("/updateuser/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.userrespon)  
def update_post(id: int, update_user: schemas.createuser, db: Session = Depends(get_db)):

    user_query = db.query(models.user).filter(models.user.id == id)

    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    user_query.update(update_user.dict(), synchronize_session=False)

    db.commit()

    return user_query.first()

@router.delete("/deleteuser/{id}", status_code=status.HTTP_201_CREATED)
def delete_post(id: int, db: Session = Depends(get_db)):

    user = db.query(models.user).filter(models.user.id == id)

    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    user.delete(synchronize_session=False)

    db.commit()
    return {'message': 'user deleted sussessfully'}
