from typing import List
from fastapi import status, HTTPException, status, HTTPException , APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (
    #     post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)): 
    # cursor.execute("""SELECT * FROM posts WHERE id = (%s)""", (str(id)))
    # post = cursor.fetchone()    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    updated_post.update(post.dict(), synchronize_session=False)                        
    db.commit()
    return updated_post.first()


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()

    return {"message" : f"Successfully deleted post with Id {id}"}
