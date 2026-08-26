from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schemas import UserCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.db_models import User, UserRole



async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    query = (
        select(User)
        .where(User.email == email)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user_data: UserCreate ) -> User:
    new_user = User(email=user_data.email, hashed_password = user_data.password, role = UserRole.VIEWER)
    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    await session.refresh(new_user)
    return new_user


async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    query = (
        select(User)
        .where(User.id == id)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()
