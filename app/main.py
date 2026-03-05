from fastapi import FastAPI, Depends
from app.database.session import test_db_connection

app = FastAPI(title="GiftPlatz API")


@app.get("/")
async def root():
    return {"message": "API запущен"}


@app.get("/health")
async def health(_: None = Depends(test_db_connection)):
    return {
        "status": "healthy",
        "database": "connected"
    }
