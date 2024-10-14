
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .model.model import Base

DATABASE_URL = "postgresql+asyncpg://postgres:boot@localhost:7432/tfree1"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
