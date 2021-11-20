from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
import psycopg2
import time
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='123456789', cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
async def root():
    return "Hello World"

@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    post = cursor.fetchall()
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (
        post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@app.get("/posts/{id}")
def get_post(id: int): 
    cursor.execute("""SELECT * FROM posts WHERE id = (%s)""", (str(id)))
    post = cursor.fetchone()    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return post


@app.put("/update_post/{id}")
def update_post(id:int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    return updated_post


@app.delete("/delete_post/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""", (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    
    return post