from fastapi import APIRouter

from app.core.logger import logger

router = APIRouter()


@router.get("/")
def root():
    logger.info("Root endpoint accessed.")

    return {
        "message": "Welcome to GitBrain 🚀"
    }