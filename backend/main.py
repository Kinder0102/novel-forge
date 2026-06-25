

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import engine, Base, SessionLocal
from models.settings import ModuleConfigModel
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL, CORS_ORIGINS
from routers import (
    worldbuilding,
    character,
    outline,
    scene,
    chapter,
    chapter_title,
    novel,
    settings,
    llm_log,
    mock,
)
from exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    
    
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="NovelForge API",
    description="AI 輔助小說創作平台後端服務",
    version="0.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


app.include_router(worldbuilding.router, prefix="/api/worldbuilding", tags=["世界觀"])
app.include_router(character.router, prefix="/api/character")
app.include_router(outline.router, prefix="/api/outline")
app.include_router(chapter_title.router, prefix="/api/chapter-title", tags=["章節標題"])
app.include_router(novel.router, prefix="/api/novels", tags=["novels"])
app.include_router(scene.router, prefix="/api/scene")
app.include_router(chapter.router, prefix="/api/chapter")
app.include_router(settings.router, prefix="/api/settings")
app.include_router(llm_log.router, prefix="/api/llm-logs", tags=["LLM Log"])
app.include_router(mock.router, prefix="/mock", tags=["Mock"])


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
