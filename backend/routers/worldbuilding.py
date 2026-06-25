from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.worldbuilding import Worldbuilding, WorldbuildingCreate, WorldbuildingUpdate, WorldbuildingResponse
from services.ai_service.generators.worldbuilding import WorldbuildingGenerator
from crud_base import CrudBase

router = APIRouter()

DELETE_OK = {"message": "已刪除"}
ENTITY = "世界觀"


@router.post("/", response_model=WorldbuildingResponse)
def create_worldbuilding(data: WorldbuildingCreate, db: Session = Depends(get_db)):
    wb = Worldbuilding(**data.model_dump())
    db.add(wb)
    db.commit()
    db.refresh(wb)
    return wb


@router.get("/", response_model=list[WorldbuildingResponse])
def list_worldbuilding(novel_id: int = Query(None), db: Session = Depends(get_db)):
    q = db.query(Worldbuilding)
    if novel_id is not None:
        q = q.filter(Worldbuilding.novel_id == novel_id)
    return q.order_by(Worldbuilding.updated_at.desc()).all()


@router.get("/{wb_id}", response_model=WorldbuildingResponse)
def get_worldbuilding(wb_id: int, db: Session = Depends(get_db)):
    return CrudBase(db).get_or_404(Worldbuilding, wb_id, ENTITY)


@router.put("/{wb_id}", response_model=WorldbuildingResponse)
def update_worldbuilding(wb_id: int, data: WorldbuildingUpdate, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    wb = crud.get_or_404(Worldbuilding, wb_id, ENTITY)
    return crud.update_and_commit(wb, data)


@router.delete("/{wb_id}")
def delete_worldbuilding(wb_id: int, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    wb = crud.get_or_404(Worldbuilding, wb_id, ENTITY)
    crud.delete_and_commit(wb)
    return DELETE_OK


class GenerateWorldbuildingRequest(BaseModel):
    novel_id: int
    theme: str = ""


@router.post("/generate", response_model=WorldbuildingResponse)
async def ai_generate_worldbuilding(req: GenerateWorldbuildingRequest, db: Session = Depends(get_db)):
    result = await WorldbuildingGenerator(db).generate(novel_id=req.novel_id, theme=req.theme)
    wb = WorldbuildingCreate(
            title=result.get("title", ""),
            genre=result.get("genre", ""),
            description=result.get("description", ""),
            setting=result.get("setting", ""),
            rules=result.get("rules", ""),
            novel_id=req.novel_id,
        )
    
    return create_worldbuilding(wb, db)


@router.post("/{wb_id}/summary", response_model=WorldbuildingResponse)
async def regenerate_worldbuilding_summary(wb_id: int, db: Session = Depends(get_db)):
    wb = CrudBase(db).get_or_404(Worldbuilding, wb_id, ENTITY)
    content = {
        "title": wb.title,
        "genre": wb.genre,
        "description": wb.description,
        "setting": wb.setting,
        "rules": wb.rules,
    }
    compact = await WorldbuildingGenerator(db).compact(content)
    return update_worldbuilding(wb_id, WorldbuildingUpdate(summary=compact), db)
