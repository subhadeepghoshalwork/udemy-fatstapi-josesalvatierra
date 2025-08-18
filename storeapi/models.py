from pydantic import BaseModel
from typing import List


class UserPostIn(BaseModel):
    body: str

class UserPostOut(UserPostIn):
    id: int

class CommentIn(BaseModel):
    post_id: int
    body: str

class CommentOut(CommentIn):
    id: int

class UserPostWithComments(BaseModel):
    post: UserPostOut
    comments: list[CommentOut]