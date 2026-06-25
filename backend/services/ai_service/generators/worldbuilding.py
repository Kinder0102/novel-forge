from services.ai_service.core import _parse_json
from .base import BaseGenerator

class WorldbuildingGenerator(BaseGenerator):
    module_name = "worldbuilding"
    temperature = 0.8

    OPTION = {
        "outputSchema": {
            "title": "世界觀名稱",
            "genre": "類型（如奇幻、科幻、武俠等）",
            "description": "世界觀整體描述（300-500字）",
            "setting": "時代與地理設定（200-400字）",
            "rules": "世界規則與法則（200-400字）",
        }
    }

    def _build_fixed_instructions(self, **kwargs) -> str:
        return "請根據以下主題概念生成一個完整的世界觀設定。"

    def _build_user_input(self, theme: str, **kwargs) -> str:
        return f"主題概念：{theme}"

    def _parse_response(self, content: str):
        return _parse_json(content, expect_list=False)

    def _compact_prompt(self) -> str:
        return "請將以下世界觀設定整理為條列式摘要，每項一行，保留關鍵名詞與核心資訊："
