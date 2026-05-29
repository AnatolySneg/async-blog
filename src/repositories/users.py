from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user import User


class UserRepository:
    pass

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieves a user instance from the database based on the provided email address.

        :param email: The email address of the user to retrieve.
        :type email: str
        :return: The user instance if a user is found, otherwise None.
        :rtype: User | None
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieves a user instance from the database based on the provided user id.

        :param user_id: The unique identifier of the user to be retrieved.
        :type user_id: int
        :return: The user object found or None if no matching user exists.
        :rtype: User | None
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(self, **user_data) -> User:
        new_user = User(**user_data)
        self.session.add(new_user)
        try:
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user
        except Exception as e:
            await self.session.rollback()
            #TODO: log error and raise http exception
            #raise
            return None