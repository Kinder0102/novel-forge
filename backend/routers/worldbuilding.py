from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.schemas import (
    Worldbuilding, WorldbuildingCreate, WorldbuildingUpdate, WorldbuildingResponse,
)
from services.ai_service import generate_worldbuilding

router = APIRouter()


@router.post("/", response_model=WorldbuildingResponse)
def create_worldbuilding(data: WorldbuildingCreate, db: Session = Depends(get_db)):
    wb = Worldbuilding(**data.model_dump())
    db.add(wb)
    db.commit()
    db.refresh(wb)
    return wb


@router.get("/", response_model=list[WorldbuildingResponse])
def list_worldbuilding(db: Session = Depends(get_db)):
    return db.query(Worldbuilding).all()


@router.get("/{wb_id}", response_model=WorldbuildingResponse)
def get_worldbuilding(wb_id: int, db: Session = Depends(get_db)):
    wb = db.query(Worldbuilding).filter(Worldbuilding.id == wb_id).first()
    if not wb:
        raise HTTPException(status_code=404, detail="世界觀不存在")
    return wb


@router.put("/{wb_id}", response_model=WorldbuildingResponse)
def update_worldbuilding(wb_id: int, data: WorldbuildingUpdate, db: Session = Depends(get_db)):
    wb = db.query(Worldbuilding).filter(Worldbuilding.id == wb_id).first()
    if not wb:
        raise HTTPException(status_code=404, detail="世界觀不存在")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(wb, key, val)
    db.commit()
    db.refresh(wb)
    return wb


@router.delete("/{wb_id}")
def delete_worldbuilding(wb_id: int, db: Session = Depends(get_db)):
    wb = db.query(Worldbuilding).filter(Worldbuilding.id == wb_id).first()
    if not wb:
        raise HTTPException(status_code=404, detail="世界觀不存在")
    db.delete(wb)
    db.commit()
    return {"message": "已刪除"}


class GenerateWorldbuildingRequest(BaseModel):
    theme: str


@router.post("/{wb_id}/generate", response_model=WorldbuildingResponse)
async def ai_generate_worldbuilding(
    wb_id: int, req: GenerateWorldbuildingRequest, db: Session = Depends(get_db)
):
    wb = db.query(Worldbuilding).filter(Worldbuilding.id == wb_id).first()
    if not wb:
        raise HTTPException(status_code=404, detail="世界觀不存在")

    result = await generate_worldbuilding(db, req.theme)
    for key in ["title", "genre", "description", "setting", "rules"]:
        if key in result:
            setattr(wb, key, result[key])
    db.commit()
    db.refresh(wb)
    return wb
