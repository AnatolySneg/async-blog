from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.post("/auth")
async def auth():
    return {"message": "Hello World"}

@auth_router.post("/register")
async def register():
    return {"message": "Registered"}

@auth_router.post("/logout")
async def logout():
    return {"message": "Logged out"}

@auth_router.post("/refresh")
async def refresh():
    return {"message": "Refreshed"}

@auth_router.post("/change-password")
async def change_password():
    return {"message": "Password changed"}

@auth_router.post("/forgot-password")
async def forgot_password():
    return {"message": "Password reset link sent"}

@auth_router.post("/reset-password")
async def reset_password():
    return {"message": "Password reset"}

@auth_router.post("/verify-email")
async def verify_email():
    return {"message": "Email verified"}

@auth_router.delete("/delete-account")
async def delete_account():
    return {"message": "Account deleted"}

