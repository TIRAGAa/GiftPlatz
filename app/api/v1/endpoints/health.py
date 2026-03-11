from fastapi import APIRouter, Depends

from app.database.session import test_db_connection

router = APIRouter(
    prefix="/health",
)


@router.get("/", summary="Проверка состояния API и базы данных")
async def health_check(_: None = Depends(test_db_connection)):
    return {
        "status": "healthy",
        "database": "connected"
    }
