from typing import List
from fastapi import FastAPI
from .models import UserPostIn, UserPostOut

app = FastAPI()

post_table = {}

@app.post("/post/", response_model=UserPostOut)
async def create_user_post(user_post: UserPostIn):
    last_record_id = len(post_table)
    new_post = {**user_post.dict(), "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post

@app.get("/post/", response_model=List[UserPostOut])
async def get_user_posts():
    return list(post_table.values())