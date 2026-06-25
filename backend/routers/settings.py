from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.schemas import ModuleConfigModel, ModuleConfigCreate, ModuleConfigResponse

router = APIRouter(prefix="/api/settings", tags=["設定"])

VALID_MODULES = ["worldbuilding", "character", "outline", "scene", "chapter", "default"]


@router.get("/modules", response_model=list[ModuleConfigResponse])
def list_module_configs(db: Session = Depends(get_db)):
    """列出所有模組設定（若某模組尚無記錄，返回空值讓前端顯示「使用預設」）"""
    configs = db.query(ModuleConfigModel).all()
    existing = {c.module_name: c for c in configs}
    result = []
    for name in VALID_MODULES:
        if name in existing:
            result.append(existing[name])
        else:
            result.append(
                ModuleConfigModel(
                    module_name=name,
                    api_key=None,
                    base_url=None,
                    model=None,
                )
            )
    return result


@router.get("/modules/{module_name}", response_model=ModuleConfigResponse)
def get_module_config(module_name: str, db: Session = Depends(get_db)):
    """取得單一模組設定"""
    if module_name not in VALID_MODULES:
        raise HTTPException(status_code=400, detail=f"無效的模組名稱：{module_name}")
    cfg = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == module_name).first()
    if not cfg:
        return ModuleConfigModel(
            module_name=module_name,
            api_key=None,
            base_url=None,
            model=None,
        )
    return cfg


@router.put("/modules/{module_name}", response_model=ModuleConfigResponse)
def upsert_module_config(module_name: str, data: ModuleConfigCreate, db: Session = Depends(get_db)):
    """更新或建立模組設定（upsert）"""
    if module_name not in VALID_MODULES:
        raise HTTPException(status_code=400, detail=f"無效的模組名稱：{module_name}")
    cfg = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == module_name).first()
    if cfg:
        if data.api_key is not None:
            cfg.api_key = data.api_key
        if data.base_url is not None:
            cfg.base_url = data.base_url
        if data.model is not None:
            cfg.model = data.model
    else:
        cfg = ModuleConfigModel(
            module_name=module_name,
            api_key=data.api_key,
            base_url=data.base_url,
            model=data.model,
        )
        db.add(cfg)
    db.commit()
    db.refresh(cfg)
    return cfg


@router.delete("/modules/{module_name}")
def delete_module_config(module_name: str, db: Session = Depends(get_db)):
    """刪除模組設定（變回 fallback 預設），但不能刪除 default"""
    if module_name == "default":
        raise HTTPException(status_code=400, detail="不可刪除 default 設定")
    if module_name not in VALID_MODULES:
        raise HTTPException(status_code=400, detail=f"無效的模組名稱：{module_name}")
    cfg = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == module_name).first()
    if not cfg:
        raise HTTPException(status_code=404, detail="該模組尚無設定")
    db.delete(cfg)
    db.commit()
    return {"message": f"已刪除 {module_name} 設定，將使用預設值"}
