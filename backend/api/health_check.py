from fastapi import APIRouter

router = APIRouter(tags=["health"], prefix="/api")

@router.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}