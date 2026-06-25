from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.chapter import ChapterContent, ChapterContentCreate, ChapterContentUpdate, ChapterContentResponse, GenerateChapterRequest
from models.outline import ChapterTitle, Outline
from services.ai_service.generators.chapter import ChapterGenerator
from crud_base import CrudBase

router = APIRouter()

DELETE_OK = {"message": "已刪除"}
ENTITY = "章節"


@router.post("/", response_model=ChapterContentResponse)
def create_chapter(data: ChapterContentCreate, db: Session = Depends(get_db)):
    chapter = ChapterContent(**data.model_dump())
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return chapter


@router.get("/", response_model=list[ChapterContentResponse])
def list_chapters(
    outline_id: int = Query(None),
    novel_id: int = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(ChapterContent).join(ChapterTitle, ChapterContent.chapter_title_id == ChapterTitle.id)
    if outline_id is not None:
        q = q.filter(ChapterTitle.outline_id == outline_id)
    return q.order_by(ChapterContent.updated_at.desc()).all()


@router.get("/{chap_id}", response_model=ChapterContentResponse)
def get_chapter(chap_id: int, db: Session = Depends(get_db)):
    return CrudBase(db).get_or_404(ChapterContent, chap_id, ENTITY)


@router.put("/{chap_id}", response_model=ChapterContentResponse)
def update_chapter(chap_id: int, data: ChapterContentUpdate, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    chapter = crud.get_or_404(ChapterContent, chap_id, ENTITY)
    return crud.update_and_commit(chapter, data)


@router.delete("/{chap_id}")
def delete_chapter(chap_id: int, db: Session = Depends(get_db)):
    crud = CrudBase(db)
    chapter = crud.get_or_404(ChapterContent, chap_id, ENTITY)
    crud.delete_and_commit(chapter)
    return DELETE_OK


@router.post("/generate", response_model=ChapterContentResponse)
async def ai_generate_chapter(req: GenerateChapterRequest, db: Session = Depends(get_db)):
    status = "completed"
    content = await ChapterGenerator(db).generate(
        novel_id=req.novel_id,
        worldbuilding_id=req.worldbuilding_id,
        chapter_title_id=req.chapter_title_id,
        description=req.description,
    )

    if req.chapter_id:
        return update_chapter(req.chapter_id, ChapterContentUpdate(content=content, status=status), db)
    
    settings = ChapterContentCreate(
        chapter_title_id=req.chapter_title_id,
        content=content,
        status=status,
    )
    return create_chapter(settings, db)


@router.post("/{chap_id}/summary", response_model=ChapterContentResponse)
async def regenerate_summary(chap_id: int, db: Session = Depends(get_db)):
    chapter = CrudBase(db).get_or_404(ChapterContent, chap_id, ENTITY)
    compacted = await ChapterGenerator(db).compact(chapter.content)
    return update_chapter(chap_id, ChapterContentUpdate(summary=compacted), db)
