from services.ai_service.core import _parse_json
from .base import BaseGenerator


class CharacterGenerator(BaseGenerator):
    module_name = "character"
    temperature = 0.9

    OPTION = {
        "outputSchema": {
            "name": "角色名稱",
            "role": "角色定位（如主角、反派、導師等）",
            "personality": "性格描述（100-200字）",
            "background": "背景故事（100-200字）",
            "appearance": "外貌描述（50-100字）",
        },
        "additional": [
            {"key": "worldbuilding", "value": "世界觀"},
        ],
    }

    def _build_fixed_instructions(self, **kwargs) -> str:
        return "請根據以下描述，生成 1 個角色。"

    def _build_user_input(self, description: str, **kwargs) -> str:
        return f"角色描述：{description}"

    def _parse_response(self, content: str):
        return _parse_json(content, expect_list=False)

    def _compact_prompt(self) -> str:
        return "請將以下角色設定整理為條列式摘要："
