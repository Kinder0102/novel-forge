from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.novel import Novel, NovelCreate, NovelUpdate, NovelResponse
from models.worldbuilding import Worldbuilding
from crud_base import CrudBase

router = APIRouter()

DELETE_OK = {"message": "已刪除"}
ENTITY = "小說"


@router.post("/", response_model=NovelResponse)
def create_novel(data: NovelCreate, db: Session = Depends(get_db)):
    create_wb = data.create_worldbuilding
    novel = Novel(
        title=data.title,
        description=data.description,
        status=data.status,
    )
    db.add(novel)
    db.flush()

    if create_wb:
        wb = Worldbuilding(
            novel_id=novel.id,
            title=novel.title,
        )
        db.add(wb)

    db.commit()
    db.refresh(novel)
    return novel


@router.get("/", response_model=list[NovelResponse])
def list_novels(db: Session = Depends(get_db)):
    return db.query(Novel).order_by(Novel.updated_at.desc()).all()


@router.get("/{novel_id}", response_model=NovelResponse)
def get_novel(novel_id: int, db: Session = Depends(get_db)):
    return CrudBase(db).get_or_404(Novel, novel_id, ENTITY)


@router.put("/{novel_id}", response_model=NovelResponse)
def update_novel(novel_id: int, data: NovelUpdate, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    novel = crud.get_or_404(Novel, novel_id, ENTITY)
    return crud.update_and_commit(novel, data)


@router.delete("/{novel_id}")
def delete_novel(novel_id: int, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    novel = crud.get_or_404(Novel, novel_id, ENTITY)
    crud.delete_and_commit(novel)
    return {"message": "已刪除"}
