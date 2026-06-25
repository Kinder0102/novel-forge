from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.outline import ChapterTitle, ChapterTitleCreate, ChapterTitleUpdate, ChapterTitleResponse, Outline
from crud_base import CrudBase

router = APIRouter()

DELETE_OK = {"message": "已刪除"}
ENTITY = "章節標題"


@router.get("/", response_model=list[ChapterTitleResponse])
def list_chapter_titles(outline_id: int = None, db: Session = Depends(get_db)):
    q = db.query(ChapterTitle)
    if outline_id is not None:
        q = q.filter(ChapterTitle.outline_id == outline_id)
    return q.order_by(ChapterTitle.idx).all()


@router.post("/", response_model=ChapterTitleResponse)
def create_chapter_title(data: ChapterTitleCreate, db: Session = Depends(get_db)):
    outline = db.query(Outline).filter(Outline.id == data.outline_id).first()
    if not outline:
        raise HTTPException(status_code=404, detail="大綱不存在")

    if data.idx is None:
        last = db.query(ChapterTitle).filter(
            ChapterTitle.outline_id == data.outline_id
        ).order_by(ChapterTitle.idx.desc()).first()
        idx = (last.idx + 1.0) if last else 1.0
    else:
        idx = data.idx

    ct = ChapterTitle(outline_id=data.outline_id, title=data.title, idx=idx)
    db.add(ct)
    db.commit()
    db.refresh(ct)
    return ct


@router.put("/{ct_id}", response_model=ChapterTitleResponse)
def update_chapter_title(ct_id: int, data: ChapterTitleUpdate, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    ct = crud.get_or_404(ChapterTitle, ct_id, ENTITY)
    crud.update_and_commit(ct, data)
    return ct


@router.delete("/{ct_id}")
def delete_chapter_title(ct_id: int, db: Session = Depends(get_db)):
    ct = db.query(ChapterTitle).filter(ChapterTitle.id == ct_id).first()
    if not ct:
        raise HTTPException(status_code=404, detail="章節標題不存在")

    db.delete(ct)
    db.commit()
    return DELETE_OK


class ReorderRequest(BaseModel):
    outline_id: int
    moved_id: int
    prev_id: Optional[int] = None
    next_id: Optional[int] = None


def _get_midpoint(
    db: Session, outline_id: int, prev_id: Optional[int], next_id: Optional[int]
) -> float:
    prev_idx: Optional[float] = None
    next_idx: Optional[float] = None

    if prev_id is not None:
        prev_ct = (
            db.query(ChapterTitle)
            .filter(ChapterTitle.id == prev_id, ChapterTitle.outline_id == outline_id)
            .first()
        )
        if prev_ct:
            prev_idx = prev_ct.idx

    if next_id is not None:
        next_ct = (
            db.query(ChapterTitle)
            .filter(ChapterTitle.id == next_id, ChapterTitle.outline_id == outline_id)
            .first()
        )
        if next_ct:
            next_idx = next_ct.idx

    if prev_idx is not None and next_idx is not None:
        return (prev_idx + next_idx) / 2.0
    if prev_idx is not None:
        return prev_idx + 1.0
    if next_idx is not None:
        return next_idx / 2.0
    return 1.0


@router.post("/reorder")
def reorder_chapter_titles(data: ReorderRequest, db: Session = Depends(get_db)):
    ct = (
        db.query(ChapterTitle)
        .filter(
            ChapterTitle.id == data.moved_id,
            ChapterTitle.outline_id == data.outline_id,
        )
        .first()
    )
    if not ct:
        raise HTTPException(status_code=404, detail="章節標題不存在")

    new_idx = _get_midpoint(db, data.outline_id, data.prev_id, data.next_id)
    ct.idx = new_idx
    db.commit()
    return {"message": "排序已更新", "new_idx": new_idx}
