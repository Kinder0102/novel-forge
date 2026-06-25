from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.scene import Scene, SceneCreate, SceneUpdate, SceneResponse
from models.outline import ChapterTitle, Outline
from crud_base import CrudBase
from services.ai_service.generators.scene import SceneGenerator
router = APIRouter()

DELETE_OK = {"message": "已刪除"}
ENTITY = "場景"


@router.post("/", response_model=SceneResponse)
def create_scene(data: SceneCreate, db: Session = Depends(get_db)):
    scene = Scene(**data.model_dump())
    db.add(scene)
    db.commit()
    db.refresh(scene)
    return scene


@router.get("/", response_model=list[SceneResponse])
def list_scenes(
    chapter_title_id: Optional[int] = Query(None),
    outline_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Scene)
    if chapter_title_id is not None:
        q = q.filter(Scene.chapter_title_id == chapter_title_id)
    if outline_id is not None:
        q = q.join(ChapterTitle, Scene.chapter_title_id == ChapterTitle.id).filter(ChapterTitle.outline_id == outline_id)
    return q.order_by(Scene.scene_number).all()


@router.get("/{scene_id}", response_model=SceneResponse)
def get_scene(scene_id: int, db: Session = Depends(get_db)):
    return CrudBase(db).get_or_404(Scene, scene_id, ENTITY)


@router.put("/{scene_id}", response_model=SceneResponse)
def update_scene(scene_id: int, data: SceneUpdate, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    scene = crud.get_or_404(Scene, scene_id, ENTITY)
    return crud.update_and_commit(scene, data)


@router.delete("/{scene_id}")
def delete_scene(scene_id: int, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    scene = crud.get_or_404(Scene, scene_id, ENTITY)
    crud.delete_and_commit(scene)
    return DELETE_OK


class BulkGenerateSceneRequest(BaseModel):
    novel_id: int
    worldbuilding_id: int
    chapter_title_id: int
    description: str = ""


@router.post("/bulk-generate", response_model=list[SceneResponse])
async def ai_bulk_generate_scenes(req: BulkGenerateSceneRequest, db: Session = Depends(get_db)):
    result = await SceneGenerator(db).generate(
        novel_id=req.novel_id,
        worldbuilding_id=req.worldbuilding_id,
        chapter_title_id=req.chapter_title_id,
        description=req.description,
    )
    max_scene = db.query(Scene.scene_number)\
        .filter(Scene.chapter_title_id == req.chapter_title_id)\
        .order_by(Scene.scene_number.desc())\
        .first()
    start_num = int(max_scene[0]) + 1 if max_scene else 1

    scenes = []
    for i, sdata in enumerate(result):
        settings = SceneCreate(
            chapter_title_id=req.chapter_title_id,
            scene_number=float(start_num + i),
            title=sdata.get("title"),
            description=sdata.get("description", ""),
        )
        scene = create_scene(settings, db)
        scenes.append(scene)
    return scenes


@router.post("/{scene_id}/summary", response_model=SceneResponse)
async def regenerate_scene_summary(scene_id: int, db: Session = Depends(get_db)):
    scene = CrudBase(db).get_or_404(Scene, scene_id, ENTITY)
    content = {
        "title": scene.title,
        "content": scene.content or "",
    }
    scene.summary = await SceneGenerator(db).compact(content)
    db.commit()
    db.refresh(scene)
    return scene
