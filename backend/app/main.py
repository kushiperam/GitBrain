from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.home import router as home_router
from app.api.routes.auth import router as auth_router
from app.api.routes.admin import router as admin_router
from app.api.routes.analysis import router as analysis_router
from app.api.routes.repository_qa import router as repository_qa_router

from app.router.repository import router as repository_router
from app.router.local_repository import router as local_repository_router

from app.core.config import settings
from app.core.logger import logger


logger.info("Starting GitBrain application...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Repository Memory Engine"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(home_router)

app.include_router(auth_router)

app.include_router(admin_router)

app.include_router(analysis_router)

app.include_router(repository_qa_router)

app.include_router(repository_router)

app.include_router(local_repository_router)


logger.info("GitBrain application started successfully.")