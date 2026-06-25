from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.schemas import (
    Character, CharacterCreate, CharacterUpdate, CharacterResponse,
)
from services.ai_service import generate_characters

router = APIRouter()


@router.post("/", response_model=CharacterResponse)
def create_character(data: CharacterCreate, db: Session = Depends(get_db)):
    char = Character(**data.model_dump())
    db.add(char)
    db.commit()
    db.refresh(char)
    return char


@router.get("/", response_model=list[CharacterResponse])
def list_characters(
    worldbuilding_id: int = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Character)
    if worldbuilding_id is not None:
        q = q.filter(Character.worldbuilding_id == worldbuilding_id)
    return q.all()


@router.get("/{char_id}", response_model=CharacterResponse)
def get_character(char_id: int, db: Session = Depends(get_db)):
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="角色不存在")
    return char


@router.put("/{char_id}", response_model=CharacterResponse)
def update_character(char_id: int, data: CharacterUpdate, db: Session = Depends(get_db)):
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="角色不存在")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(char, key, val)
    db.commit()
    db.refresh(char)
    return char


@router.delete("/{char_id}")
def delete_character(char_id: int, db: Session = Depends(get_db)):
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="角色不存在")
    db.delete(char)
    db.commit()
    return {"message": "已刪除"}


class GenerateCharactersRequest(BaseModel):
    worldbuilding_id: int
    description: str = ""
    worldbuilding_context: str = ""


@router.post("/generate", response_model=CharacterResponse)
async def ai_generate_characters(req: GenerateCharactersRequest, db: Session = Depends(get_db)):
    try:
        result = await generate_characters(db, req.worldbuilding_context, req.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 生成角色失敗：{str(e)}")

    if not isinstance(result, dict):
        raise HTTPException(status_code=500, detail="AI 回傳格式錯誤，無法解析角色")

    char = Character(
        worldbuilding_id=req.worldbuilding_id,
        name=result.get("name", ""),
        role=result.get("role", ""),
        personality=result.get("personality", ""),
        background=result.get("background", ""),
        appearance=result.get("appearance", ""),
    )
    db.add(char)
    db.commit()
    db.refresh(char)
    return char
