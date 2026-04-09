from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI Interview Prep - FastAPI",
        "version": "1.0.0"
    }


@router.get("/")
async def root():
    return {
        "message": "AI Interview Prep FastAPI Service",
        "docs": "/docs",
        "health": "/health"
    }
