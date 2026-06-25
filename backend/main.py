from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import engine, Base, SessionLocal
from routers import worldbuilding, character, outline, scene, chapter, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _init_default_module_config()
    yield


def _init_default_module_config():
    """首次啟動時若 default 不存在，自動插入一筆 default 設定"""
    from models.schemas import ModuleConfigModel
    from config import AI_API_KEY, AI_BASE_URL, AI_MODEL

    db = SessionLocal()
    try:
        existing = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == "default").first()
        if not existing:
            default_cfg = ModuleConfigModel(
                module_name="default",
                api_key=AI_API_KEY,
                base_url=AI_BASE_URL,
                model=AI_MODEL,
            )
            db.add(default_cfg)
            db.commit()
    finally:
        db.close()


app = FastAPI(title="NovelForge API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(worldbuilding.router, prefix="/api/worldbuilding", tags=["世界觀"])
app.include_router(character.router, prefix="/api/character", tags=["角色"])
app.include_router(outline.router, prefix="/api/outline", tags=["大綱"])
app.include_router(scene.router, prefix="/api/scene", tags=["場景"])
app.include_router(chapter.router, prefix="/api/chapter", tags=["章節"])
app.include_router(settings.router)
