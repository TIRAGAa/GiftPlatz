from typing import Annotated
from fastapi import FastAPI, Depends
import uvicorn

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession, create_async_engine,
                                    async_sessionmaker)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///gifts.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SeesionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class GiftModel(Base):
    __tablename__ = 'gifts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    price: Mapped[int]
    weight: Mapped[int]


@app.post(
        '/setup_database',
        summary="Настроить базу данных",
        tags=["Настройка"]
    )
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/gifts", summary="Получить список всех подарков", tags=["Подарки"])
async def read_gifts(session: SeesionDep):
    query = select(GiftModel)
    result = await session.execute(query)
    return result.scalars().all()


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
