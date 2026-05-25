from fastapi import FastAPI
from api.routers.auth import auth_router
from api.routers.blog import blog_router


app = FastAPI(title="", debug=True, version="0.1.0")

app.include_router(auth_router)
app.include_router(blog_router)


@app.get("/")
async def root():
    return {"message": "Welcome to async_blog! Be polite and respectful to other members."}

