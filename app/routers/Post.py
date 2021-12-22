# from codecs import decode
from typing import List
from fastapi import  status, HTTPException, Depends, APIRouter
from jose.utils import timedelta_total_seconds
# from random import randrange
from sqlalchemy.orm import Session
from starlette.responses import Response
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter()

@router.post("/newpost", status_code=status.HTTP_201_CREATED, response_model=schemas.post)
def create_post(post: schemas.Createpost, db: Session = Depends(get_db)):
    new_post = models.post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/getpost", response_model=List[schemas.post])
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.post).all()
    return post

@router.get("/post/{id}", response_model=schemas.post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.post).filter(models.post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
    return post

@router.put("/updatepost/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.post)  
def update_post(id: int, update_post: schemas.Createpost, db: Session = Depends(get_db)):

    post_query = db.query(models.post).filter(models.post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post_query.update(update_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

@router.delete("/deletepost/{id}", status_code=status.HTTP_201_CREATED)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.post).filter(models.post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post.delete(synchronize_session=False)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
