from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import app_config

engine = create_async_engine(str(app_config.postgresql_dsn), echo=app_config.debug)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
