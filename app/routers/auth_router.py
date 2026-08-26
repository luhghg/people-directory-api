from fastapi import APIRouter, Depends
from app.core.security import login_user, register_user
from app.schemas.user_schemas import UserResponse, UserCreate, UserLogin
from app.schemas.token_chems import Token
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(path="/register", response_model=UserResponse)
async def register (session: Annotated[AsyncSession, Depends(get_session)], user_data: UserCreate) -> UserResponse:
    return await register_user(session=session, user_data=user_data)

@router.post(path="/login", response_model=Token)
async def login(session: Annotated[AsyncSession, Depends(get_session)], login_data: UserLogin) -> Token:
    return await login_user(session=session, login_data=login_data)
