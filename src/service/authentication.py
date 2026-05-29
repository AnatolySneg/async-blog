from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from src.core.config import settings

class SecurityUtils:
    """
    Utility class for handling security operations including password
    hashing, password verification, and JWT token management.

    This class provides methods to securely hash passwords, verify
    passwords using hashed values, create JSON Web Tokens (JWT) for
    authentication, and decode JWT tokens to extract its payload.

    :ivar NONE
    :type NONE: NONE
    """
    # Hashing password
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Setup password hashing context 

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._pwd_context.verify(plain_password, hashed_password)

    # JWT token
    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Create an access token containing specified data, with a default or custom expiration time.

        This method generates a JSON Web Token (JWT), encoding provided payload data and
        assigning either a default expiration duration or a custom expiration when specified.

        :param data: A dictionary containing the data to be encoded in the JWT payload.
        :type data: dict
        :param expires_delta: Optional custom expiration timedelta. Defaults to None.
        :type expires_delta: timedelta | None
        :return: Encoded JWT token as a string.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta  # Set custom expiration duration
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # Default expiration

        to_encode.update({"exp": expire})  # Add expiration time to the token payload

        jwt_token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)  # Encode JWT token

        return jwt_token

    @classmethod
    def decode_access_token(cls, token: str) -> dict | None:
        """
        Decodes the provided JWT token to extract payload details. This method attempts to decode the
        JSON Web Token (JWT) using the configured secret key and algorithm and returns the payload
        details if the token is valid. If the token is expired or invalid, `None` is returned.

        :param token: the JWT token as a string to be decoded.
        :type token: str
        :return: a dictionary containing the decoded payload from the token if decoding is successful,
                 or `None` if the token is invalid or expired.
        :rtype: dict | None
        """
        # Decode the provided JWT token to extract payload details
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])  # Decode token
            return payload
        except jwt.ExpiredSignatureError:
            #TODO: Raising error with http status code
            return None
        except jwt.InvalidTokenError:
            # TODO: Raising error with http status code
            return None
