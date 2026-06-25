from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.outline import Outline, OutlineCreate, OutlineUpdate, OutlineResponse, ChapterTitle
from crud_base import CrudBase
from services.ai_service.generators.outline import OutlineGenerator
from utils import get_novel_id_by_ct

router = APIRouter()

DELETE_OK = {"message": "已刪除"}
ENTITY = "大綱"


@router.post("/", response_model=OutlineResponse)
def create_outline(data: OutlineCreate, db: Session = Depends(get_db)):
    outline = Outline(**data.model_dump())
    db.add(outline)
    db.commit()
    db.refresh(outline)
    return outline


@router.get("/", response_model=list[OutlineResponse])
def list_outlines(
    worldbuilding_id: Optional[int] = Query(None),
    novel_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Outline)
    if worldbuilding_id is not None:
        q = q.filter(Outline.worldbuilding_id == worldbuilding_id)
    if novel_id is not None:
        q = q.filter(Outline.novel_id == novel_id)
    return q.order_by(Outline.updated_at.desc()).all()


@router.get("/{outline_id}", response_model=OutlineResponse)
def get_outline(outline_id: int, db: Session = Depends(get_db)):
    return CrudBase(db).get_or_404(Outline, outline_id, ENTITY)


@router.put("/{outline_id}", response_model=OutlineResponse)
def update_outline(outline_id: int, data: OutlineUpdate, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    outline = crud.get_or_404(Outline, outline_id, ENTITY)
    return crud.update_and_commit(outline, data)


@router.delete("/{outline_id}")
def delete_outline(outline_id: int, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    outline = crud.get_or_404(Outline, outline_id, ENTITY)
    crud.delete_and_commit(outline)
    return DELETE_OK


class GenerateOutlineRequest(BaseModel):
    novel_id: int
    worldbuilding_id: int
    description: str = ""
    character_ids: Optional[list[int]] = None


@router.post("/generate", response_model=OutlineResponse)
async def ai_generate_outline(req: GenerateOutlineRequest, db: Session = Depends(get_db)):
    result = await OutlineGenerator(db).generate(
        novel_id=req.novel_id,
        worldbuilding_id=req.worldbuilding_id,
        description=req.description,
        character_ids=req.character_ids,
    )
    outline_data = OutlineCreate(
        novel_id=req.novel_id,
        worldbuilding_id=req.worldbuilding_id,
        title=result.get("title", ""),
        description=result.get("description", ""),
    )

    outline = create_outline(outline_data, db)

    for i, ct_data in enumerate(result.get("chapters", [])):
        ct = ChapterTitle(
            outline_id=outline.id,
            idx=float(i),
            title=ct_data.get("title", f"第{i+1}章"),
        )
        db.add(ct)
    db.commit()
    db.refresh(ct)
    return outline


@router.post("/{outline_id}/summary", response_model=OutlineResponse)
async def regenerate_outline_summary(outline_id: int, db: Session = Depends(get_db)):
    outline = CrudBase(db).get_or_404(Outline, outline_id, ENTITY)
    outline.summary = await OutlineGenerator(db).compact(outline.description)
    db.commit()
    db.refresh(outline)
    return outline
