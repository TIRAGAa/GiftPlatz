import uvicorn
from fastapi import FastAPI

from app.api.v1.endpoints import health, setup


app = FastAPI(
    title="GiftPlatz API",
    description="API для проекта GiftPlatz",
    version="0.1.0"
)

app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Остновные"]
)

app.include_router(setup.router)


if __name__ in '__main__':
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
