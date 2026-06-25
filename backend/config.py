import os
import warnings
from dotenv import load_dotenv

load_dotenv()


_default_db = os.path.join(os.path.dirname(__file__), "novel.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{_default_db}")


_old_api_key = os.environ.get("AI_API_KEY")
_old_base_url = os.environ.get("AI_BASE_URL")

AI_API_KEY = os.environ.get("OPENAI_API_KEY") or _old_api_key or "sk-placeholder"
AI_BASE_URL = os.environ.get("OPENAI_BASE_URL") or _old_base_url or "https://api.openai.com/v1"

if _old_api_key and not os.environ.get("OPENAI_API_KEY"):
    warnings.warn(
        "環境變數 AI_API_KEY 已棄用，請改用 OPENAI_API_KEY",
        DeprecationWarning,
    )
if _old_base_url and not os.environ.get("OPENAI_BASE_URL"):
    warnings.warn(
        "環境變數 AI_BASE_URL 已棄用，請改用 OPENAI_BASE_URL",
        DeprecationWarning,
    )


SERVER_PORT = int(os.environ.get("PORT") or os.environ.get("BACKEND_PORT", "8001"))

AI_MODEL = os.environ.get("AI_MODEL", "gpt-4o")
AI_TIMEOUT = int(os.environ.get("AI_TIMEOUT", "300"))
MOCK_AI = os.environ.get("MOCK_AI", "false").lower() in ("true", "1", "yes")


CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")




DEFAULT_PROMPTS: dict[str, dict[str, str]] = {
    "worldbuilding": {
        "system_prompt": "你是專業小說世界觀架構師，擅長建構奇幻、科幻、武俠等各類小說的世界觀。請一律以繁體中文回覆。",
        "user_prompt": "",
    },
    "character": {
        "system_prompt": "你是專業小說角色設計師，擅長創造立體、有深度的角色。請一律以繁體中文回覆。",
        "user_prompt": "",
    },
    "outline": {
        "system_prompt": "你是專業小說大綱規劃師，擅長設計引人入勝的故事結構。請嚴格遵循提供的世界觀設定來構思大綱，確保故事背景、規則、地理等要素與世界觀一致。請一律以繁體中文回覆。",
        "user_prompt": "",
    },
    "scene": {
        "system_prompt": "你是專業小說場景規劃師，擅長將章節拆解為具體場景。請一律以繁體中文回覆。",
        "user_prompt": "",
    },
    "chapter": {
        "system_prompt": "你是專業小說作家，擅長撰寫長篇敘事。請一律以繁體中文回覆，不使用 Markdown 語法。",
        "user_prompt": "",
    },
    "compact": {
        "system_prompt": "你是專業內容摘要師，擅長將冗長的創作素材濃縮為精簡摘要。請一律以繁體中文回覆。",
        "user_prompt": "",
    },
    "chapter_summary": {
        "system_prompt": "你是專業小說編輯，擅長為章節撰寫精簡摘要。請一律以繁體中文回覆。",
        "user_prompt": "",
    },
}
