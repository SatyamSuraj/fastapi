from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body, Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from .database import engine, get_db
from . import models, schemas, utils
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return "Hello World"



