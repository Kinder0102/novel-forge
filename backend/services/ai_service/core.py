
import httpx
import json
import re
import time
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError
from models.settings import ModuleConfigModel
from models.task_log import LLMCallLog
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL, AI_TIMEOUT, DEFAULT_PROMPTS


async def _get_module_config(db: Session, module_name: str) -> dict:
    
    
    module_cfg = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == module_name).first()
    
    default_cfg = db.query(ModuleConfigModel).filter(ModuleConfigModel.module_name == "default").first()

    def _resolve(key: str) -> str | None:
        
        if module_cfg:
            val = getattr(module_cfg, key, None)
            if val:
                return val
        
        if default_cfg:
            val = getattr(default_cfg, key, None)
            if val:
                return val
        
        env_map = {"api_key": AI_API_KEY, "base_url": AI_BASE_URL, "model": AI_MODEL}
        if key in env_map:
            return env_map[key]
        
        prompts = DEFAULT_PROMPTS.get(module_name, {})
        return prompts.get(key)

    return {
        "api_key": _resolve("api_key"),
        "base_url": _resolve("base_url"),
        "model": _resolve("model"),
        "system_prompt": _resolve("system_prompt"),
        "user_prompt": _resolve("user_prompt_template"),
    }


async def _call_ai(
    db: Session,
    module_name: str,
    messages: list[dict],
    api_key: str,
    base_url: str,
    model: str,
    temperature: float = 0.8,
    max_tokens: int = 32768,
) -> str:
    
    llm_url = f"{base_url}/chat/completions"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    
    log_entry = LLMCallLog(
        module_name=module_name,
        model=model,
        llm_url=llm_url,
        status="pending",
        request_payload=json.dumps(
            {"messages": messages, "temperature": temperature, "max_tokens": max_tokens},
            ensure_ascii=False,
        ),
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=AI_TIMEOUT) as client:
            resp = await client.post(llm_url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            if not content:
                finish_reason = data["choices"][0].get("finish_reason", "unknown")
                usage = data.get("usage", {})
                raise ValueError(
                    f"LLM 回覆內容為空 (finish_reason={finish_reason}, "
                    f"prompt_tokens={usage.get('prompt_tokens')}, "
                    f"completion_tokens={usage.get('completion_tokens')})"
                )
            duration_ms = int((time.time() - start) * 1000)
            usage = data.get("usage", {})

            
            log_entry.status = "success"
            log_entry.response_content = content
            log_entry.prompt_tokens = usage.get("prompt_tokens")
            log_entry.completion_tokens = usage.get("completion_tokens")
            log_entry.total_tokens = usage.get("total_tokens")
            log_entry.duration_ms = duration_ms
            try:
                db.commit()
            except StaleDataError:
                db.rollback()
                pass  

            
            _trim_logs(db)

            return content
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)

        
        log_entry.status = "error"
        log_entry.error_message = str(e)
        log_entry.duration_ms = duration_ms
        try:
            db.commit()
        except StaleDataError:
            db.rollback()
            pass

        _trim_logs(db)
        raise


def _trim_logs(db: Session):
    
    from sqlalchemy import text
    db.execute(text(
        "DELETE FROM llm_call_log WHERE id <= ("
        "SELECT id FROM llm_call_log ORDER BY id DESC LIMIT 1 OFFSET 50"
        ")"
    ))
    db.commit()


def schema_to_prompt(schema: dict, *, indent: int = 0) -> str:
    





    if not schema:
        return ""
    prefix = " " * indent
    lines = []
    
    if indent == 0:
        lines.append("請以 JSON 格式回覆，不要加任何說明文字，包含以下欄位：")
    for field, desc in schema.items():
        if isinstance(desc, list):
            
            lines.append(f"{prefix}- {field}: JSON 陣列，每項包含：")
            if desc and isinstance(desc[0], dict):
                lines.append(schema_to_prompt(desc[0], indent=indent + 2))
            else:
                lines.append(f"{prefix}  - （陣列元素）: {desc[0] if desc else '任意值'}")
        else:
            lines.append(f"{prefix}- {field}: {desc}")
    return "\n".join(lines)


class _ParseError(Exception):
    

    def __init__(self, message: str, raw_text: str = ""):
        super().__init__(message)
        self.raw_text = raw_text


def _parse_json(text: str, expect_list: bool = True) -> dict | list:
    







    def _try_parse(raw: str) -> dict | list | None:
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return None

    def _extract_balanced(text: str, open_char: str, close_char: str) -> str | None:
        
        start = text.find(open_char)
        if start == -1:
            return None
        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(text)):
            c = text[i]
            if escape:
                escape = False
                continue
            if c == '\\':
                escape = True
                continue
            if c == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == open_char:
                depth += 1
            elif c == close_char:
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
        return None

    
    result = _try_parse(text)
    if result is not None:
        return _wrap(result, expect_list)

    
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.DOTALL)
    if match:
        result = _try_parse(match.group(1))
        if result is not None:
            return _wrap(result, expect_list)

    
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        block = text[first_brace:last_brace + 1]
        result = _try_parse(block)
        if result is not None:
            return _wrap(result, expect_list)

    
    balanced = _extract_balanced(text, '{', '}')
    if balanced:
        result = _try_parse(balanced)
        if result is not None:
            return _wrap(result, expect_list)
    balanced = _extract_balanced(text, '[', ']')
    if balanced:
        result = _try_parse(balanced)
        if result is not None:
            return _wrap(result, expect_list)

    
    snippet = text[:500] if len(text) > 500 else text
    raise _ParseError(f"無法從 AI 回覆中解析 JSON（前 500 字元）: {snippet}")


def _wrap(result, expect_list: bool) -> dict | list:
    if expect_list and isinstance(result, dict):
        return [result]
    return result
