from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from source.core.settings import settings


DATABASE_URL = settings.DATABASE_URL


async_engine = create_async_engine(DATABASE_URL)


async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
