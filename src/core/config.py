from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Unified configuration interface.
    Currently retrieves data from environment variables (with priority) and from the .env file.
    In the future, it will be easy to add YAML or other sources to model_config.
    """

    # Database settings with type validation
    POSTGRES_USER: str = Field(..., description="Database user")
    POSTGRES_PASSWORD: str = Field(..., description="Database password")
    POSTGRES_DB: str = Field(..., description="Database name")
    POSTGRES_HOST: str = Field(..., description="Database host")
    POSTGRES_PORT: int = Field(5432, description="Database port")

    # Configuration for where pydantic will retrieve data from
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # Ignore any extra variables in the .env file
        # that are not described in this class
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        """Constructs a URL for SQLAlchemy connection based on basic parameters."""
        return f"database+databa://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
