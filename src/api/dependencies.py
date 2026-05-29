from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.repositories.users import UserRepository

from src.database.db import get_db

class RepoManager:

    @staticmethod
    async def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
        return UserRepository(session)
