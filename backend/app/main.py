from fastapi import FastAPI

from app.api.routes.home import router as home_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Repository Memory Engine"
)

app.include_router(home_router)