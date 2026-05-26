from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.core.config import settings

DATABASE_URL = settings.database_url

# Create an asynchronous engine (Engine)
# echo=True will make SQLAlchemy output all SQL queries to the console. Ideal for learning.
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.LOCAL_DEVELOPMENT,  # Enable logging of SQL queries if local development is enabled

    pool_size=settings.POSTGRES_POOL_SIZE,  # Base number of database connections
    max_overflow=settings.POSTGRES_MAX_OVERFLOW,  # Max additional connections beyond pool_size
    pool_timeout=settings.POSTGRES_POOL_TIMEOUT,  # Time (in seconds) to wait for a connection before error

    pool_pre_ping=True  # Enable connection pre-ping to ensure connections are valid
)

# Create an asynchronous session factory (Sessionmaker)
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Deep magic: protects against asynchronous lazy loading errors
)


async def get_db() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with async_session_maker() as session:
        yield session
