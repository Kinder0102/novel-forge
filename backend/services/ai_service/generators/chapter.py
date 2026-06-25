from sqlalchemy.orm import Session
from .base import BaseGenerator
from models.scene import Scene


class ChapterGenerator(BaseGenerator):
    module_name = "chapter"
    temperature = 0.9

    OPTION = {
        "outputSchema": {},
        "additional": [
            {"key": "outline", "value": "大綱"},
            {"key": "previous_summary", "value": "前一章摘要"},
            {"key": "scene", "value": "場景規劃"},
            {"key": "writing_style", "value": "寫作風格"},
        ],
    }

    def _build_fixed_instructions(self, **kwargs) -> str:
        return "根據以下規劃，撰寫完整章節內容（約 2000-4000 字）。"

    def _build_user_input(self, description: str = "", **kwargs) -> str:
        return f"章節描述：{description}" if description else ""

    def _parse_response(self, content: str):
        return content

    def _compact_prompt(self) -> str:
        return "請將以下章節內容摘要為 100-200 字的精簡描述，保留關鍵情節與轉折："
