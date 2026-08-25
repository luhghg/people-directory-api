from app.repositories.user_repo import get_user_by_email
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.db.session import async_session

import asyncio

async def testing(session: AsyncSession, email: str ="string@gmail.com"):
    res = await get_user_by_email(session=session, email=email)
    return res

async def main():

    async with async_session() as session:

        user = await testing(session=session)
        print(f"{user}")


asyncio.run(main())

#ДОПИСАТЬ ЧЕРНОВИК ПРАВЛЬНО ЧТОБЫ ПРОВЕРИТЬ РАБОТАЕТ ЛИ ФУНКЦИЯ ЕМЕЙЛ
# И ДАЛЬШЕ ДДЕДЛАТЬ ВСЮ АУНТЕФИКАИЮ И АВТОРИЗАЦИЮ
