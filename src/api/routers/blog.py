from fastapi import APIRouter

blog_router = APIRouter()


@blog_router.post("/post")
async def create_post():
    return {"message": "Created post"}

@blog_router.put("/post/{post_id}")
async def update_post(post_id: int):
    return {"message": f"Updated post {post_id}"}

@blog_router.delete("/post/{post_id}")
async def delete_post(post_id: int):
    return {"message": f"Deleted post {post_id}"}

@blog_router.get("/posts")
async def get_posts():
    return {"message": "Posts"}

@blog_router.get("/post/{post_id}")
async def get_post_detail(post_id: int):
    return {"message": f"Post {post_id}"}
