

from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException


class CrudBase:
    


    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_404(self, model: type, entity_id: int, entity_name: str) -> Any:
        obj = self.db.query(model).filter(model.id == entity_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{entity_name}不存在")
        return obj

    def update_and_commit(self, obj: Any, data: Any) -> Any:
        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, val)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_and_commit(self, obj: Any) -> None:
        self.db.delete(obj)
        self.db.commit()
