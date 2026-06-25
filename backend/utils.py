

from sqlalchemy.orm import Session
from models.outline import ChapterTitle, Outline


def get_novel_id_by_ct(db: Session, chapter_title_id: int) -> int | None:
    
    ct = db.query(ChapterTitle).filter(ChapterTitle.id == chapter_title_id).first()
    if not ct:
        return None
    outline = db.query(Outline).filter(Outline.id == ct.outline_id).first()
    if not outline:
        return None
    return outline.novel_id
