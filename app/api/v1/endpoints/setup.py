from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database.session import get_db

router = APIRouter(
    prefix="/api/v1/setup",
    tags=["setup", "admin"]
)


@router.post(
    "/create-warehouse-table/",
    summary="Создать таблицу warehouse_items (если ещё не существует)"
)
async def create_warehouse_table(db: AsyncSession = Depends(get_db)):
    try:
        check_query = text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'warehouse_items'
            );
        """)
        result = await db.execute(check_query)
        exists = result.scalar()

        if exists:
            return {"message": "Таблица warehouse_items уже существует"}

        create_query = text("""
CREATE TABLE warehouse_items (
    id                SERIAL PRIMARY KEY,
    name              VARCHAR(200) NOT NULL,
    quantity_pieces   INTEGER,
    quantity_kg       DOUBLE PRECISION NOT NULL,
    price             DOUBLE PRECISION NOT NULL,
    created_at        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
""")
        await db.execute(create_query)
        await db.commit()

        return {"message": "Таблица warehouse_items успешно создана"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании таблицы: {str(e)}"
        )
