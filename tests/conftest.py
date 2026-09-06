from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker)
import pytest
from app.db.session import Base
from main import app
from httpx import AsyncClient, ASGITransport
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator




@pytest.fixture
async def prepare_database():
    global async_engine
    async_engine = create_async_engine(url="postgresql+asyncpg://user:postgres3211@localhost:5432/people_directory_api_test", echo=False)
    global async_session
    async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


    yield

    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(prepare_database) -> AsyncGenerator[AsyncSession, None] :

    async with async_session() as session:
        yield session


@pytest.fixture
async def client(prepare_database):


    async def overrides_session():
        async with async_session() as session:
            yield session


    app.dependency_overrides[get_session] = overrides_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test" ) as ac:
            yield ac


    app.dependency_overrides.clear()
