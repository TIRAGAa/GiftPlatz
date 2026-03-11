from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Корневая страница API")
async def root():
    return {"message": "GiftPlatz API работает"}
