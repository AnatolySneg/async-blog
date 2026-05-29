from src.models.user import User

class AuthenticationService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.user_repo.get_by_id(user_id)

    async def register(self, email: str, password: str) -> User:
        pass # TODO: Implement user registration

    async def login(self, email: str, password: str) -> User:
        pass # TODO: Implement user login



