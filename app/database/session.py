from sqlalchemy.ext.asyncio import (create_async_engine, AsyncSession,
                                    async_sessionmaker)
from sqlalchemy import text
from fastapi import Depends, HTTPException

from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
)


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def test_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(status_code=503,
                            detail=f"База недоступна: {str(e)}")
