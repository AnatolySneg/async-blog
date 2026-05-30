from fastapi import APIRouter, Depends, status

from src.validation.auth import RegistrationResponse
from src.validation.base import StandardResponse
from src.validation import UserRegisterSchema
from src.service.authentication import AuthenticationService
from src.api.dependencies import ServiceManager
from src.utils.response_handler import ApiResponse

auth_router = APIRouter()

@auth_router.post("/auth", response_model=StandardResponse)
async def auth():
    return {"message": "Hello World"}

@auth_router.post("/register", response_model=StandardResponse[RegistrationResponse])
async def register(user_data: UserRegisterSchema, service: AuthenticationService = Depends(ServiceManager.get_auth_service)):
    try:
        result = await service.register_user(user_data.model_dump())
        return ApiResponse.success(data=result, message="User registered successfully.", status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        return ApiResponse.failure(status_code=status.HTTP_400_BAD_REQUEST, message="Registration failed.", detail=str(e))

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

