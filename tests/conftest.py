from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker)
import pytest
from app.db.session import Base
from main import app
from fastapi.testclient import TestClient

async_engine = create_async_engine(url="postgresql+asyncpg://user:postgres3211@localhost:5432/people_directory_api_test", echo=False)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

@pytest.fixture
async def prepare_database():
    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)



@pytest.fixture
async def db_session():
    async with async_session as session:
        yield session

@pytest.fixture
async def client(db_session):

    def overrides():
        yield session

    app.dependency_overrides[get_session] = overrides

    with TestClient(app) test_client:
        yield test_client

    app.dependency_overrides.clear()
