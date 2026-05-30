from fastapi import APIRouter

posts_router = APIRouter()


@posts_router.post("/post")
async def create_post():
    return {"message": "Created post"}

@posts_router.put("/post/{post_id}")
async def update_post(post_id: int):
    return {"message": f"Updated post {post_id}"}

@posts_router.delete("/post/{post_id}")
async def delete_post(post_id: int):
    return {"message": f"Deleted post {post_id}"}

@posts_router.get("/posts")
async def get_posts():
    return {"message": "Posts"}

@posts_router.get("/post/{post_id}")
async def get_post_detail(post_id: int):
    return {"message": f"Post {post_id}"}
