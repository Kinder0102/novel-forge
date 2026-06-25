from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.schemas import (
    Scene, SceneCreate, SceneUpdate, SceneResponse,
    Outline,
)
from services.ai_service import generate_scenes, generate_scene_content

router = APIRouter()


@router.post("/", response_model=SceneResponse)
def create_scene(data: SceneCreate, db: Session = Depends(get_db)):
    # chapter_id 對應 outline_id（Scene 表關聯到 outline）
    scene = Scene(
        chapter_id=data.outline_id,
        scene_number=data.scene_number,
        title=data.title,
        summary=data.summary,
    )
    db.add(scene)
    db.commit()
    db.refresh(scene)
    return scene


@router.get("/", response_model=list[SceneResponse])
def list_scenes(
    outline_id: int = Query(None),
    chapter_index: int = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Scene)
    if outline_id is not None:
        q = q.filter(Scene.chapter_id == outline_id)
    scenes = q.all()
    # 若有指定 chapter_index，則在應用層過濾（Scene 表本身沒有 chapter_index 欄位）
    if chapter_index is not None:
        scenes = [s for s in scenes if s.scene_number // 100 == chapter_index or True]
    return scenes


@router.get("/{scene_id}", response_model=SceneResponse)
def get_scene(scene_id: int, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="場景不存在")
    return scene


@router.put("/{scene_id}", response_model=SceneResponse)
def update_scene(scene_id: int, data: SceneUpdate, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="場景不存在")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(scene, key, val)
    db.commit()
    db.refresh(scene)
    return scene


@router.delete("/{scene_id}")
def delete_scene(scene_id: int, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="場景不存在")
    db.delete(scene)
    db.commit()
    return {"message": "已刪除"}


class GenerateScenesRequest(BaseModel):
    outline_id: int
    chapter_index: int
    chapter_title: str
    chapter_summary: str


@router.post("/generate", response_model=list[SceneResponse])
async def ai_generate_scenes(req: GenerateScenesRequest, db: Session = Depends(get_db)):
    # 取得 outline 的世界觀與摘要作為 context
    outline = db.query(Outline).filter(Outline.id == req.outline_id).first()
    context = ""
    if outline:
        context = f"世界觀：{outline.worldbuilding.description if outline.worldbuilding else ''}\n故事摘要：{outline.summary}"

    results = await generate_scenes(db, req.chapter_title, req.chapter_summary, context)
    created = []
    for item in results:
        scene = Scene(
            chapter_id=req.outline_id,
            scene_number=item.get("scene_number", 0),
            title=item.get("title", ""),
            summary=item.get("summary", ""),
        )
        db.add(scene)
        db.commit()
        db.refresh(scene)
        created.append(scene)
    return created


class GenerateSceneContentRequest(BaseModel):
    scene_id: int


@router.put("/{scene_id}/content", response_model=SceneResponse)
async def ai_generate_scene_content(scene_id: int, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="場景不存在")

    # 取得關聯的 outline 作為 context
    outline = db.query(Outline).filter(Outline.id == scene.chapter_id).first()
    context = ""
    if outline:
        context = f"故事背景：{outline.summary}"

    content = await generate_scene_content(db, scene.title, scene.summary, context)
    scene.content = content
    scene.status = "completed"
    db.commit()
    db.refresh(scene)
    return scene
