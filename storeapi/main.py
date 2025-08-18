from typing import List
from fastapi import FastAPI
from .models import UserPostIn, UserPostOut

from fastapi import FastAPI
from .routers.post import router as post_router

app = FastAPI()
app.include_router(post_router)