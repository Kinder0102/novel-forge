from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.character import Character, CharacterCreate, CharacterUpdate, CharacterResponse
from services.ai_service.generators.character import CharacterGenerator
from crud_base import CrudBase

router = APIRouter()

DELETE_OK = {"message": "已刪除"}
ENTITY = "角色"


@router.post("/", response_model=CharacterResponse)
def create_character(data: CharacterCreate, db: Session = Depends(get_db)):
    char = Character(**data.model_dump())
    db.add(char)
    db.commit()
    db.refresh(char)
    return char


@router.get("/", response_model=list[CharacterResponse])
def list_characters(
    worldbuilding_id: Optional[int] = Query(None),
    novel_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Character)
    if worldbuilding_id is not None:
        q = q.filter(Character.worldbuilding_id == worldbuilding_id)
    if novel_id is not None:
        q = q.filter(Character.novel_id == novel_id)
    return q.order_by(Character.updated_at.desc()).all()


@router.get("/{char_id}", response_model=CharacterResponse)
def get_character(char_id: int, db: Session = Depends(get_db)):
    return CrudBase(db).get_or_404(Character, char_id, ENTITY)


@router.put("/{char_id}", response_model=CharacterResponse)
def update_character(char_id: int, data: CharacterUpdate, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    char = crud.get_or_404(Character, char_id, ENTITY)
    return crud.update_and_commit(char, data)


@router.delete("/{char_id}")
def delete_character(char_id: int, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    char = crud.get_or_404(Character, char_id, ENTITY)
    crud.delete_and_commit(char)
    return DELETE_OK


class GenerateCharactersRequest(BaseModel):
    description: str = ""
    novel_id: int
    worldbuilding_id: int


@router.post("/generate", response_model=CharacterResponse)
async def ai_generate_characters(req: GenerateCharactersRequest, db: Session = Depends(get_db)):
    result = await CharacterGenerator(db).generate(worldbuilding_id=req.worldbuilding_id, description=req.description)
    char_data = CharacterCreate(
        novel_id=req.novel_id,
        worldbuilding_id=req.worldbuilding_id,
        name=result.get("name", ""),
        role=result.get("role") or "",
        personality=result.get("personality") or "",
        background=result.get("background") or "",
        appearance=result.get("appearance") or "",
    )
    return create_character(char_data, db)

@router.post("/{char_id}/summary", response_model=CharacterResponse)
async def regenerate_character_summary(char_id: int, db: Session = Depends(get_db)):
    char = CrudBase(db).get_or_404(Character, char_id, ENTITY)
    content = {
        "name": char.name,
        "role": char.role,
        "personality": char.personality,
        "background": char.background,
        "appearance": char.appearance,
    }
    compact = await CharacterGenerator(db).compact(content)
    return update_character(char_id, CharacterUpdate(summary=compact), db)
