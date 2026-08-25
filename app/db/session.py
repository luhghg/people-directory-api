from sqlalchemy.ext.asyncio import (AsyncSession, create_async_engine,
                                     async_sessionmaker)
from sqlalchemy.orm import DeclarativeBase
from collections.abc import AsyncGenerator
from app.core.config import settings

async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=False)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
