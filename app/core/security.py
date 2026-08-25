from fastapi.security import OAuth2PasswordBearer
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schemas import UserCreate, UserResponse, UserLogin
from app.repositories.user_repo import get_user_by_email, create_user
from fastapi import HTTPException, status
from app.models.db_models import User
from app.schemas.token_chems import Token
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ph = PasswordHasher()



def hash_pass_argon2(password: str):
    return ph.hash(password=password)

def verify_pass_argon2(plain_pass: str, hashed_pass: str) -> bool:
    try:
        return ph.verify(hash=hashed_pass, password=plain_pass)
    except VerifyMismatchError:
        return False

async def regiter_user(session: AsyncSession, user_data: UserCreate) -> UserResponse:
    if await get_user_by_email(session = session, email = user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email alresdy registred")
    hash_pass = hash_pass_argon2(password=user_data.password)
    user_data.password = hash_pass
    create_new_user = await create_user(session=session, user_data=user_data)
    user_response = UserResponse(id=create_new_user.id, created_at=create_new_user.created_at)
    return user_response


async def create_access_token(data: dict[str, str | int | datetime]) -> Token:
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": exp})
    encoded_jwt = jwt.encode(payload=to_encode, key=settings.SECRET_KEY, algorithm="HS256")
    jwt_token = Token(access_token=encoded_jwt)
    return jwt_token


async def login_user(session: AsyncSession, login_data: UserLogin) -> Token:
    user = await get_user_by_email(session=session, email=login_data.email)
    if not user or not verify_pass_argon2(plain_pass=login_data.password, hashed_pass=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password")
    access_token = await create_access_token(data={"sub": str(user.id)})
    return  access_token
