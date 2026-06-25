import os

DATABASE_URL = "sqlite+aiosqlite:////Users/kinder/KS/practice/novel/backend/novel.db"
AI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-placeholder")
AI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
AI_MODEL = os.environ.get("AI_MODEL", "gpt-4o")
