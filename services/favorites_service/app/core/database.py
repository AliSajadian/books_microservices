from sqlalchemy.orm import declarative_base 
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from .config import settings


async_engine = create_async_engine(url=settings.ASYNC_DATABASE_URL, echo=True, future=True, isolation_level="SERIALIZABLE")

AsyncSessionLocal = async_sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

