from services.ai_service.core import _parse_json
from .base import BaseGenerator


class SceneGenerator(BaseGenerator):
    module_name = "scene"
    temperature = 0.8

    OPTION = {
        "outputSchema": {
            "scene_number": "場景編號（從1.0開始，支援小數插入如1.5）",
            "title": "場景標題",
            "description": "場景摘要（50-150字）",
        },
        "additional": [
            {"key": "outline", "value": "大綱"},
            {"key": "previous_summary", "value": "前一章摘要"},
            {"key": "writing_style", "value": "寫作風格"},
        ],
    }

    def _build_fixed_instructions(self, **kwargs) -> str:
        return "將章節拆分為 3-5 個場景。"

    def _build_user_input(self, description: str = "", **kwargs) -> str:
        return f"場景描述：{description}" if description else ""

    def _parse_response(self, content: str):
        return _parse_json(content, expect_list=True)

    def _compact_prompt(self) -> str:
        return "請將以下場景清單整理為條列式摘要，每場景一行（編號. 標題 — 一句摘要）："
