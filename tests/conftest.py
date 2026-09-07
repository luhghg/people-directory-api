from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker)
import pytest
from app.db.session import Base
from main import app
from httpx import AsyncClient, ASGITransport
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
import jwt
from sqlalchemy import update
from app.models.db_models import User, UserRole
from app.core.config import settings
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError



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


@pytest.fixture
async def sama_voydet(client):
    response_reg = await client.post(
        "/auth/register", json={"email": "tet12345@gmail.com", "password": "12345test"}
    )
    if response_reg.status_code == 400:
        raise Exception("Email already registred")
    response_log = await client.post(
                                    "/auth/login", data={"username": "tet12345@gmail.com", "password": "12345test"}
                                    )
    data = response_log.json()
    token = data["access_token"]
    return token


@pytest.fixture
async def sama_voydet_hr(sama_voydet, db_session):
    token = sama_voydet
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    user_id_str = str(user_id)
    query = (
            update(User)
            .where(User.id == int(user_id_str))
            .values(role = UserRole.HR)
            )
    await db_session.execute(query)
    await db_session.commit()
    return token

@pytest.fixture
async def sama_voydet_id_usera(sama_voydet, db_session):
    token = sama_voydet
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    user_id_int = int(user_id)

    return user_id_int
