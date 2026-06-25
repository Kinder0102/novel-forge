from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.schemas import (
    ChapterContent, ChapterContentCreate, ChapterContentUpdate, ChapterContentResponse,
    Outline,
)
from services.ai_service import generate_chapter

router = APIRouter()


@router.post("/", response_model=ChapterContentResponse)
def create_chapter(data: ChapterContentCreate, db: Session = Depends(get_db)):
    chap = ChapterContent(**data.model_dump())
    db.add(chap)
    db.commit()
    db.refresh(chap)
    return chap


@router.get("/", response_model=list[ChapterContentResponse])
def list_chapters(
    outline_id: int = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(ChapterContent)
    if outline_id is not None:
        q = q.filter(ChapterContent.outline_id == outline_id)
    return q.order_by(ChapterContent.chapter_index).all()


@router.get("/{chap_id}", response_model=ChapterContentResponse)
def get_chapter(chap_id: int, db: Session = Depends(get_db)):
    chap = db.query(ChapterContent).filter(ChapterContent.id == chap_id).first()
    if not chap:
        raise HTTPException(status_code=404, detail="章節不存在")
    return chap


@router.put("/{chap_id}", response_model=ChapterContentResponse)
def update_chapter(chap_id: int, data: ChapterContentUpdate, db: Session = Depends(get_db)):
    chap = db.query(ChapterContent).filter(ChapterContent.id == chap_id).first()
    if not chap:
        raise HTTPException(status_code=404, detail="章節不存在")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(chap, key, val)
    db.commit()
    db.refresh(chap)
    return chap


@router.delete("/{chap_id}")
def delete_chapter(chap_id: int, db: Session = Depends(get_db)):
    chap = db.query(ChapterContent).filter(ChapterContent.id == chap_id).first()
    if not chap:
        raise HTTPException(status_code=404, detail="章節不存在")
    db.delete(chap)
    db.commit()
    return {"message": "已刪除"}


class GenerateChapterRequest(BaseModel):
    outline_id: int
    chapter_index: int
    chapter_title: str
    chapter_summary: str
    context: str = ""


@router.post("/generate", response_model=ChapterContentResponse)
async def ai_generate_chapter(req: GenerateChapterRequest, db: Session = Depends(get_db)):
    content = await generate_chapter(db, req.chapter_title, req.chapter_summary, req.context)
    chap = ChapterContent(
        outline_id=req.outline_id,
        chapter_index=req.chapter_index,
        title=req.chapter_title,
        content=content,
        status="completed",
    )
    db.add(chap)
    db.commit()
    db.refresh(chap)
    return chap


@router.get("/export/{outline_id}")
def export_chapters(outline_id: int, db: Session = Depends(get_db)):
    chapters = (
        db.query(ChapterContent)
        .filter(ChapterContent.outline_id == outline_id)
        .order_by(ChapterContent.chapter_index)
        .all()
    )
    if not chapters:
        raise HTTPException(status_code=404, detail="該大綱尚無章節內容")

    lines = []
    for ch in chapters:
        lines.append(f"第{ch.chapter_index + 1}章 {ch.title}")
        lines.append("")
        lines.append(ch.content)
        lines.append("")
        lines.append("─" * 40)
        lines.append("")

    return PlainTextResponse("\n".join(lines), media_type="text/plain; charset=utf-8")
