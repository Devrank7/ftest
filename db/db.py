import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .model.model import Base
postgres_host = os.getenv("POSTGRES_HOST", "localhost")
postgres_port = os.getenv("POSTGRES_PORT", 7432)
postgres_user = os.getenv("POSTGRES_USER", "postgres")
postgres_password = os.getenv("POSTGRES_PASSWORD", "boot")
postgres_db = os.getenv("POSTGRES_DB", "tfree1")
DATABASE_URL = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
