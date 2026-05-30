from fastapi import FastAPI
from src.api.routers.auth import auth_router
from src.api.routers.posts import posts_router


app = FastAPI(title="Async Blog API", debug=True, version="0.1.0")

app.include_router(auth_router)
app.include_router(posts_router)


@app.get("/")
async def root():
    return {"message": "Welcome to async_blog! Be polite and respectful to other members."}

