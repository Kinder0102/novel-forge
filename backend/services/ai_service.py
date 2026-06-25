import httpx
import json
import re
from sqlalchemy.orm import Session
from models.schemas import ModuleConfigModel
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL


async def _get_module_config(db: Session, module_name: str) -> dict:
    """取得模組的 API 設定，含 fallback 邏輯"""
    # 1. 查詢目標模組設定
    module_cfg = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == module_name).first()
    # 2. 查詢 default 設定（若存在的話）
    default_cfg = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == "default").first()

    def _resolve(key: str) -> str | None:
        # 先取目標模組值
        if module_cfg:
            val = getattr(module_cfg, key, None)
            if val:
                return val
        # fallback 到 default
        if default_cfg:
            val = getattr(default_cfg, key, None)
            if val:
                return val
        # 最終 fallback 到 config.py
        env_map = {"api_key": AI_API_KEY, "base_url": AI_BASE_URL, "model": AI_MODEL}
        return env_map.get(key)

    return {
        "api_key": _resolve("api_key"),
        "base_url": _resolve("base_url"),
        "model": _resolve("model"),
    }


async def _call_ai(
    messages: list[dict],
    api_key: str,
    base_url: str,
    model: str,
    temperature: float = 0.8,
    max_tokens: int = 4096,
) -> str:
    """通用 AI 呼叫方法"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(f"{base_url}/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


def _parse_json(text: str, expect_list: bool = True) -> dict | list:
    """嘗試從 AI 返回的文字中提取 JSON。
    expect_list=True 時，若 AI 回傳單一物件（dict），自動包裝成 [dict] 返回。
    支援 Qwen 思考模型：自動跳過前綴的推理文字，提取末尾 JSON。
    """
    def _try_parse(raw: str) -> dict | list | None:
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return None

    # 1. 直接解析全文
    result = _try_parse(text)
    if result is not None:
        return _wrap(result, expect_list)

    # 2. 提取 ```json / ``` 代碼塊
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.DOTALL)
    if match:
        result = _try_parse(match.group(1))
        if result is not None:
            return _wrap(result, expect_list)

    # 3. 從最後一個 { 或 [ 開始提取（處理思考模型前綴文字）
    for char in ("{", "["):
        idx = text.rfind(char)
        if idx != -1:
            result = _try_parse(text[idx:])
            if result is not None:
                return _wrap(result, expect_list)

    # 4. 正則匹配第一組 { ... } 或 [ ... ]（貪婪）
    brace_match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text, re.DOTALL)
    if brace_match:
        result = _try_parse(brace_match.group(1))
        if result is not None:
            return _wrap(result, expect_list)

    raise ValueError(f"無法從 AI 回覆中解析 JSON: {text[:200]}...")


def _wrap(result, expect_list: bool) -> dict | list:
    if expect_list and isinstance(result, dict):
        return [result]
    return result


async def generate_worldbuilding(db: Session, theme: str) -> dict:
    """根據主題概念生成世界觀"""
    cfg = await _get_module_config(db, "worldbuilding")
    messages = [
        {
            "role": "system",
            "content": "你是專業小說世界觀架構師，擅長建構奇幻、科幻、武俠等各類小說的世界觀。請一律以繁體中文回覆。",
        },
        {
            "role": "user",
            "content": f"""請根據以下主題概念生成一個完整的世界觀設定。請以 JSON 格式回覆，包含以下欄位：
- title: 世界觀名稱
- genre: 類型（如奇幻、科幻、武俠等）
- description: 世界觀整體描述（300-500字）
- setting: 時代與地理設定（200-400字）
- rules: 世界規則與法則（200-400字）

主題概念：{theme}

請只輸出 JSON，不要加任何說明文字。""",
        },
    ]
    content = await _call_ai(messages, cfg["api_key"], cfg["base_url"], cfg["model"], temperature=0.8)
    return _parse_json(content)


async def generate_characters(db: Session, worldbuilding_context: str, description: str = "") -> dict:
    """根據世界觀生成單一角色"""
    cfg = await _get_module_config(db, "character")
    description_hint = f"\n額外描述要求：{description}" if description else ""
    messages = [
        {
            "role": "system",
            "content": "你是專業小說角色設計師，擅長創造立體、有深度的角色。請一律以繁體中文回覆。",
        },
        {
            "role": "user",
            "content": f"""請根據以下世界觀，生成 1 個角色。角色需包含以下欄位：
- name: 角色名稱
- role: 角色定位（如主角、反派、導師等）
- personality: 性格描述（100-200字）
- background: 背景故事（100-200字）
- appearance: 外貌描述（50-100字）

請以 JSON 物件格式回覆，例如：
{{"name": "...", "role": "...", "personality": "...", "background": "...", "appearance": "..."}}

世界觀：{worldbuilding_context}{description_hint}

請只輸出 JSON，不要加任何說明文字。""",
        },
    ]
    content = await _call_ai(messages, cfg["api_key"], cfg["base_url"], cfg["model"], temperature=0.9)
    return _parse_json(content, expect_list=False)


async def generate_outline(db: Session, context: str, description: str = "") -> dict:
    """生成單一章節的故事大綱"""
    cfg = await _get_module_config(db, "outline")
    description_hint = f"\n大綱描述：{description}" if description else ""
    messages = [
        {
            "role": "system",
            "content": "你是專業小說大綱規劃師，擅長設計引人入勝的故事結構。請一律以繁體中文回覆。",
        },
        {
            "role": "user",
            "content": f"""請根據以下背景資訊，生成一個包含 1 個章節的故事大綱。請以 JSON 格式回覆，包含以下欄位：
- title: 故事標題
- summary: 故事整體摘要（200-400字）
- chapters: 章節列表，每個章節含 title（章節標題）和 summary（章節摘要，100-200字）

背景資訊：{context}{description_hint}

請只輸出 JSON，不要加任何說明文字。""",
        },
    ]
    content = await _call_ai(messages, cfg["api_key"], cfg["base_url"], cfg["model"], temperature=0.85)
    return _parse_json(content)


async def generate_scenes(db: Session, chapter_title: str, chapter_summary: str, context: str) -> list[dict]:
    """將章節拆成多個場景"""
    cfg = await _get_module_config(db, "scene")
    messages = [
        {
            "role": "system",
            "content": "你是專業小說場景規劃師，擅長將章節拆解為具體場景。請一律以繁體中文回覆。",
        },
        {
            "role": "user",
            "content": f"""請將以下章節拆分為 3-5 個場景。每個場景需包含：
- scene_number: 場景編號（從1開始）
- title: 場景標題
- summary: 場景摘要（50-150字）

請以 JSON 陣列格式回覆。

章節標題：{chapter_title}
章節摘要：{chapter_summary}
背景資訊：{context}

請只輸出 JSON，不要加任何說明文字。""",
        },
    ]
    content = await _call_ai(messages, cfg["api_key"], cfg["base_url"], cfg["model"], temperature=0.8)
    return _parse_json(content, expect_list=True)


async def generate_scene_content(db: Session, scene_title: str, scene_summary: str, context: str) -> str:
    """生成單一場景的具體內容（約 800-1500 字）"""
    cfg = await _get_module_config(db, "scene")
    messages = [
        {
            "role": "system",
            "content": "你是專業小說作家，擅長撰寫生動、細膩的敘事文字。請一律以繁體中文回覆，不使用 Markdown 語法。",
        },
        {
            "role": "user",
            "content": f"""請根據以下場景資訊，撰寫一個完整的場景內容（約 800-1500 字）。請直接寫出故事內文，不要加標題或說明。

場景標題：{scene_title}
場景摘要：{scene_summary}
背景資訊：{context}""",
        },
    ]
    content = await _call_ai(messages, cfg["api_key"], cfg["base_url"], cfg["model"], temperature=0.9, max_tokens=4096)
    return content.strip()


async def generate_chapter(db: Session, chapter_title: str, chapter_summary: str, context: str) -> str:
    """生成完整章節內容（約 2000-4000 字）"""
    cfg = await _get_module_config(db, "chapter")
    messages = [
        {
            "role": "system",
            "content": "你是專業小說作家，擅長撰寫長篇敘事。請一律以繁體中文回覆，不使用 Markdown 語法。",
        },
        {
            "role": "user",
            "content": f"""請根據以下章節資訊，撰寫一個完整的章節內容（約 2000-4000 字）。請直接寫出故事內文，不要加標題或說明。

章節標題：{chapter_title}
章節摘要：{chapter_summary}
背景資訊：{context}""",
        },
    ]
    content = await _call_ai(messages, cfg["api_key"], cfg["base_url"], cfg["model"], temperature=0.9, max_tokens=8192)
    return content.strip()
