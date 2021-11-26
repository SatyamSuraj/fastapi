from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/Health_check")
async def root():
    return "Health Check Success"
