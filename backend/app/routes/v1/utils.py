from fastapi import APIRouter


utils_router = APIRouter(prefix="/utils", tags=["utils"])


@utils_router.get("/health-check/")
async def health_check() -> bool:
    return True
