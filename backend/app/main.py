from fastapi import FastAPI

from app.api.routes.home import router as home_router
from app.api.routes.auth import router as auth_router
from app.api.routes.admin import router as admin_router
from app.router.repository import router as repository_router

from app.core.config import settings
from app.core.logger import logger

logger.info("Starting GitBrain application...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Repository Memory Engine"
)

app.include_router(home_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(repository_router)

logger.info("GitBrain application started successfully.")
