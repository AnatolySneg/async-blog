from src.models.user import User
from src.utils.security import SecurityHandler
from src.validation.auth import RegistrationResponse

class AuthenticationService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.user_repo.get_by_id(user_id)

    async def register_user(self, user_data: dict) -> dict:
        existing_user: User|None = await self.user_repo.get_by_email(user_data['email'])
        if existing_user:
            raise ValueError('User with this email already exists') # TODO: raise http error

        raw_password = user_data.pop('password')
        user_data["hashed_password"] = SecurityHandler.hash_password(raw_password)

        user: User = await self.user_repo.create_user(**user_data)

        access_token: str = SecurityHandler.create_access_token(data={"sub": str(user.id), "role": user.role})

        return RegistrationResponse(user=user, access_token=access_token).model_dump()

    async def login(self, email: str, password: str) -> User:
        pass # TODO: Implement user login



