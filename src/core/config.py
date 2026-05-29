import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Unified configuration interface.
    Currently retrieves data from environment variables (with priority) and from the .env file.
    In the future, it will be easy to add YAML or other sources to model_config.
    """
    # General settings
    PROJECT_NAME: str = "FastAPI Async-blog"
    # Uses to prevent leaking of sensitive information
    PRODUCTION: bool = Field(..., description="Whether the app is running in production mode")
    # Uses for local console outputs and debugging
    LOCAL_DEVELOPMENT: bool = False if PRODUCTION else Field(False, description="Whether the app is running in local development mode")

    # JWT settings
    JWT_SECRET_KEY: str = Field(..., description="Secret key for JWT authentication")
    JWT_ALGORITHM: str = Field("HS256", description="Algorithm used for JWT authentication")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, description="Expiration time of access tokens in minutes")

    # Database settings with type validation
    POSTGRES_USER: str = Field(..., description="Database user")
    POSTGRES_PASSWORD: str = Field(..., description="Database password")
    POSTGRES_DATABASE: str = Field(..., description="Database name")
    POSTGRES_HOST: str = Field(..., description="Database host")
    POSTGRES_PORT: int = Field(5432, description="Database port")

    # SQLAlchemy pool settings
    # Base number of connections
    POSTGRES_POOL_SIZE: int = Field(5, description="Base number of database connections in the pool")
    # Maximum number of additional connections during peak load
    POSTGRES_MAX_OVERFLOW: int = Field(10, description="Maximum number of temporary connections above pool_size")
    # Number of seconds a query will wait in queue if all connections are busy
    POSTGRES_POOL_TIMEOUT: int = Field(30, description="Seconds to wait before giving up on getting a connection")

    # Configuration for where pydantic will retrieve data from
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        # Ignore any extra variables in the .env file
        # that are not described in this class
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        """Constructs a URL for SQLAlchemy connection based on basic parameters."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

settings = Settings()
