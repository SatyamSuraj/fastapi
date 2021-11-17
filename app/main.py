from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None


@app.get("/")
async def root():
    return "Hello World"

@app.get("/posts")
def get_post():
    return "Posts"

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    print(post.dict())
    return post.dict()

def find_post(id):
    return None

@app.get("/posts/{id}")
def get_post(id: int): 
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return int(id)

@app.delete("/delete_post/{id}")
def delete_post(id: int):
    return "Post Deleted"