from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.settings import ModuleConfigModel, ModuleConfigCreate, ModuleConfigResponse
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL, DEFAULT_PROMPTS

router = APIRouter()

VALID_MODULES = ["worldbuilding", "character", "outline", "scene", "chapter", "compact", "default"]

FALLBACK_DEFAULTS = {
    "api_key": AI_API_KEY,
    "base_url": AI_BASE_URL,
    "model": AI_MODEL,
}



def _build_dummy(module_name: str) -> dict:
    result: dict = {"module_name": module_name}
    if module_name == "default":
        result.update(FALLBACK_DEFAULTS)
    else:
        defaults = DEFAULT_PROMPTS.get(module_name, {})
        result["system_prompt"] = defaults.get("system_prompt", "")
        result["user_prompt_template"] = defaults.get("user_prompt_template", "")
    return result


def _orm_to_dict(cfg: ModuleConfigModel) -> dict:
    defaults = DEFAULT_PROMPTS.get(cfg.module_name, {})
    result = {
        "id": cfg.id,
        "module_name": cfg.module_name,
        "api_key": cfg.api_key,
        "base_url": cfg.base_url,
        "model": cfg.model,
        "system_prompt": cfg.system_prompt or defaults.get("system_prompt", ""),
        "user_prompt_template": cfg.user_prompt_template or defaults.get("user_prompt_template", ""),
        "updated_at": cfg.updated_at.isoformat() if cfg.updated_at else None,
    }
    if cfg.module_name == "default":
        if not result["api_key"]:
            result["api_key"] = AI_API_KEY
        if not result["base_url"]:
            result["base_url"] = AI_BASE_URL
        if not result["model"]:
            result["model"] = AI_MODEL
    return result


@router.get("/modules", response_model=list[ModuleConfigResponse])
def list_module_configs(db: Session = Depends(get_db)):
    configs = db.query(ModuleConfigModel).all()
    result = []
    seen = {c.module_name for c in configs}
    for name in VALID_MODULES:
        if name in seen:
            result.append(_orm_to_dict(next(c for c in configs if c.module_name == name)))
        else:
            result.append(_build_dummy(name))
    return result


@router.get("/modules/{module_name}", response_model=ModuleConfigResponse)
def get_module_config(module_name: str, db: Session = Depends(get_db)):
    if module_name not in VALID_MODULES:
        raise HTTPException(status_code=400, detail=f"無效的模組名稱：{module_name}")
    config = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == module_name).first()
    if not config:
        return _build_dummy(module_name)
    return _orm_to_dict(config)


@router.put("/modules/{module_name}", response_model=ModuleConfigResponse)
def upsert_module_config(module_name: str, data: ModuleConfigCreate, db: Session = Depends(get_db)):
    if module_name not in VALID_MODULES:
        raise HTTPException(status_code=400, detail=f"無效的模組名稱：{module_name}")
    config = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == module_name).first()
    if config:
        for field in ("api_key", "base_url", "model", "system_prompt", "user_prompt_template"):
            val = getattr(data, field, None)
            if val is not None:
                setattr(config, field, val)
    else:
        config = ModuleConfigModel(module_name=module_name, **data.model_dump())
        db.add(config)
    db.commit()
    db.refresh(config)
    return config


@router.delete("/modules/{module_name}")
def delete_module_config(module_name: str, db: Session = Depends(get_db)):
    if module_name == "default":
        raise HTTPException(status_code=400, detail="不可刪除 default 設定")
    if module_name not in VALID_MODULES:
        raise HTTPException(status_code=400, detail=f"無效的模組名稱：{module_name}")
    config = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == module_name).first()
    if config:
        db.delete(config)
        db.commit()
    return {"message": f"已刪除 {module_name} 設定，將使用預設值"}
