import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.schemas import (
    Outline, OutlineCreate, OutlineUpdate, OutlineResponse,
)
from services.ai_service import generate_outline

router = APIRouter()


def _enrich_outline(outline: Outline) -> dict:
    """將 Outline ORM 物件轉為 dict，並解析 chapters_json"""
    data = {
        "id": outline.id,
        "worldbuilding_id": outline.worldbuilding_id,
        "title": outline.title,
        "summary": outline.summary,
        "chapters_json": outline.chapters_json,
        "created_at": outline.created_at,
        "updated_at": outline.updated_at,
    }
    try:
        data["chapters"] = json.loads(outline.chapters_json)
    except (json.JSONDecodeError, TypeError):
        data["chapters"] = []
    return data


@router.post("/")
def create_outline(data: OutlineCreate, db: Session = Depends(get_db)):
    outline = Outline(**data.model_dump())
    db.add(outline)
    db.commit()
    db.refresh(outline)
    return _enrich_outline(outline)


@router.get("/")
def list_outlines(
    worldbuilding_id: int = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Outline)
    if worldbuilding_id is not None:
        q = q.filter(Outline.worldbuilding_id == worldbuilding_id)
    return [_enrich_outline(o) for o in q.all()]


@router.get("/{outline_id}")
def get_outline(outline_id: int, db: Session = Depends(get_db)):
    outline = db.query(Outline).filter(Outline.id == outline_id).first()
    if not outline:
        raise HTTPException(status_code=404, detail="大綱不存在")
    return _enrich_outline(outline)


@router.put("/{outline_id}")
def update_outline(outline_id: int, data: OutlineUpdate, db: Session = Depends(get_db)):
    outline = db.query(Outline).filter(Outline.id == outline_id).first()
    if not outline:
        raise HTTPException(status_code=404, detail="大綱不存在")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(outline, key, val)
    db.commit()
    db.refresh(outline)
    return _enrich_outline(outline)


@router.delete("/{outline_id}")
def delete_outline(outline_id: int, db: Session = Depends(get_db)):
    outline = db.query(Outline).filter(Outline.id == outline_id).first()
    if not outline:
        raise HTTPException(status_code=404, detail="大綱不存在")
    db.delete(outline)
    db.commit()
    return {"message": "已刪除"}


class GenerateOutlineRequest(BaseModel):
    worldbuilding_id: int
    context: str = ""
    description: str = ""


@router.post("/generate")
async def ai_generate_outline(req: GenerateOutlineRequest, db: Session = Depends(get_db)):
    result = await generate_outline(db, req.context, req.description)
    chapters = result.get("chapters", [])
    outline = Outline(
        worldbuilding_id=req.worldbuilding_id,
        title=result.get("title", ""),
        summary=result.get("summary", ""),
        chapters_json=json.dumps(chapters, ensure_ascii=False),
    )
    db.add(outline)
    db.commit()
    db.refresh(outline)
    return _enrich_outline(outline)
