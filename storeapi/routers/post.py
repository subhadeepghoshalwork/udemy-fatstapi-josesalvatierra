from fastapi import APIRouter
from typing import List
from ..models import UserPostIn, UserPostOut, CommentOut, CommentIn,UserPostWithComments
from fastapi import HTTPException

router = APIRouter()

comment_table = {}
post_table = {}

def find_post_by_id(post_id: int):
    return post_table.get(post_id)
@router.post("/post/", response_model=UserPostOut, status_code=201)
async def create_user_post(user_post: UserPostIn):
    last_record_id = len(post_table)
    new_post = {**user_post.model_dump(), "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post

@router.get("/post/", response_model=List[UserPostOut])
async def get_user_posts():
    return list(post_table.values())

@router.post("/comment/", response_model=CommentOut, status_code=201)
async def create_comment(comment: CommentIn):
    if not find_post_by_id(comment.post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    last_record_id = len(comment_table)
    new_comment = {**comment.model_dump(), "id": last_record_id}
    comment_table[last_record_id] = new_comment
    return new_comment

@router.get("/comment/", response_model=List[CommentOut])
async def get_comments():
    return list(comment_table.values())


@router.get("/post/{post_id}/comments/", response_model=List[CommentOut])
async def get_comments_on_post(post_id: int):
    if post_id not in post_table:
        raise HTTPException(status_code=404, detail="Post not found at all")
    return [comment for comment in comment_table.values() if comment["post_id"] == post_id]


@router.get("/post/{post_id}/", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = post_table.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }