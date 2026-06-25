from services.ai_service.core import _parse_json
from .base import BaseGenerator


class OutlineGenerator(BaseGenerator):
    module_name = "outline"
    temperature = 0.85

    OPTION = {
        "outputSchema": {
            "title": "故事標題",
            "description": "故事整體摘要（200-400字）",
            "chapters": [
                {"title": "章節標題"},
            ],
        },
        "additional": [
            {"key": "worldbuilding", "value": "世界觀"},
            {"key": "writing_style", "value": "寫作風格"},
            {"key": "character", "value": "角色資訊"},
        ],
    }

    def _build_fixed_instructions(self, **kwargs) -> str:
        return "生成一個包含 1 個章節的故事大綱。"

    def _build_user_input(self, description: str = "", **kwargs) -> str:
        return f"大綱描述：{description}" if description else ""

    def _parse_response(self, content: str):
        return _parse_json(content, expect_list=False)

    def _compact_prompt(self) -> str:
        return "請將以下故事大綱精簡, 過濾掉不必要的描述："
