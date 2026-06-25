from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.task_log import LLMCallLog, LLMCallLogResponse

router = APIRouter(tags=["llm_log"])


@router.get("/", response_model=list[LLMCallLogResponse])
def list_llm_logs(db: Session = Depends(get_db)):
    return db.query(LLMCallLog).order_by(LLMCallLog.created_at.desc()).limit(50).all()


@router.delete("/")
def delete_llm_logs(db: Session = Depends(get_db)):
    db.query(LLMCallLog).filter(LLMCallLog.status != "pending").delete(synchronize_session=False)
    db.commit()
    return {"message": "已清除所有 LLM 呼叫記錄"}
