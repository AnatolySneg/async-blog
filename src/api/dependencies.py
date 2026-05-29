from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.users import UserRepository
from src.service.authentication import AuthenticationService

from src.database.db import get_db

from fastapi.security import OAuth2PasswordBearer
from src.utils.security import SecurityHandler
from src.models.user import User
from src.models.enums import UserRole

# Specify the login path (Swagger will use it for the Authorize button)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class RepoManager:

    @staticmethod
    async def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
        return UserRepository(session)


class ServiceManager:
    @staticmethod
    async def get_auth_service(user_repo: UserRepository = Depends(RepoManager.get_user_repository)) -> AuthenticationService:
        return AuthenticationService(user_repo)


class AuthDependency:
    @staticmethod
    async def get_current_user(
            token: str = Depends(oauth2_scheme),
            auth_service: AuthenticationService = Depends(ServiceManager.get_auth_service),
    ) -> User:
        """
        Retrieve the current authenticated user based on the provided token and authentication service.

        This method utilizes the provided token to decode the user's information securely.
        It ensures the user is active and authorized.
        Will raise HTTP-related exceptions when critical conditions are unmet.

        :param token: The access token for authentication.
        :param auth_service: Dependency-injected service for authentication operations.
        :return: The authenticated user object if the credentials are valid.
        :rtype: User
        :raises HTTPException: If token validation fails, user is not found, inactive, banned, or deleted.
        """
        # Decode the access token to extract user payload
        payload = SecurityHandler.decode_access_token(token)

        # Handle the case when the token is invalid or cannot be decoded
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        # Extract user ID from the token payload
        user_id: str = payload.get("sub")

        # Check if user ID is missing in the token payload
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Retrieve the user associated with the extracted user ID
        user = await auth_service.get_user_by_id(int(user_id))

        # Handle the case when the user does not exist
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Check if the user is inactive
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

        # Deny access if the user is banned
        if user.role == UserRole.banned:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is banned")

        # Deny access if the user account is deleted
        if user.role == UserRole.deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is deleted")

        # Return the authenticated user object
        return user

    async def is_moderator(self) -> bool:
        pass # TODO: Implement is_moderator