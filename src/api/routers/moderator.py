from fastapi import APIRouter

moderate_router = APIRouter()


@moderate_router.get("/moderate")
async def moderate():
    return {"message": "Hello World"}

@moderate_router.post("/mute_user")
async def mute_user():
    return {"message": "User muted"}

@moderate_router.post("/ban_user")
async def ban_user():
    return {"message": "User banned"}

@moderate_router.post("/delete_post")
async def delete_post():
    return {"message": "Post deleted"}

@moderate_router.post("/delete_comment")
async def delete_comment():
    return {"message": "Comment deleted"}

@moderate_router.post("/report_user")
async def report_user():
    return {"message": "User reported"}

@moderate_router.delete("/delete_account")
async def delete_account():
    return {"message": "Account deleted"}