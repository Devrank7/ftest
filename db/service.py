from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.enum.enums import Category, Language
from db.model.model import User


class UserService:

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        super().__init__()
        self.session = session

    async def create(self, base: User) -> None:
        async with self.session() as session:
            async with session.begin():
                session.add(base)
        await session.commit()

    async def read(self, user_id: int) -> User:
        async with self.session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user

    async def delete(self, user_id: int) -> None:
        async with self.session() as session:
            query = delete(User).where(User.id == user_id)
            await session.execute(query)
            await session.commit()

    async def update(self, user_id: int, base: User) -> None:
        async with self.session() as session:
            user = await session.get(User, user_id)
            user.copy_data(other_usr=base)
            await session.commit()

    async def update_category(self, user_id: int, category: Category) -> None:
        async with self.session() as session:
            user = await session.get(User, user_id)
            user.category = category
            await session.commit()

    async def update_language(self, user_id: int, language: Language) -> None:
        async with self.session() as session:
            user = await session.get(User, user_id)
            if user:
                old_language = user.lang
                user.lang = language
                if old_language != language:
                    await session.commit()

    async def exists(self, user_id: int) -> bool:
        async with self.session() as session:
            result = await session.get(User, user_id)
            print('result', result)
            return result is not None
