import bcrypt
from datetime import datetime, timedelta, timezone
import jwt
from src.core.config import settings
from fastapi import HTTPException,status

class SecurityHandler:


    @classmethod
    def hash_password(cls, password: str) -> str:
        # Encode the password as bytes using UTF-8
        password_bytes = password.encode("utf-8")
        # Generate a random salt
        salt = bcrypt.gensalt()
        # Hash the password bytes with the generated salt
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        # Decode the hashed password to a UTF-8 string and return it
        return hashed_password.decode("utf-8")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        # Convert the plain password to bytes using UTF-8 encoding
        password_bytes = plain_password.encode("utf-8")
        # Convert the hashed password to bytes using UTF-8 encoding
        hashed_password_bytes = hashed_password.encode("utf-8")
        try:
            # Verify the plain password against the hashed password
            return bcrypt.checkpw(password_bytes, hashed_password_bytes)
        except Exception:
            # Return False if an exception occurs during verification
            return False

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
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
