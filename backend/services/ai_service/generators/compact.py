from sqlalchemy.orm import Session
from .base import BaseGenerator


class CompactGenerator(BaseGenerator):
    module_name = "compact"
    temperature = 0.3

    OPTION = {
        "outputSchema": {},
        "additional": [],
    }

    def _compact_prompt(self) -> str:
        return ""

    def _build_fixed_instructions(self, **kwargs) -> str:
        return "請根據以下格式要求，將原始內容整理為精簡摘要。"

    def _build_user_input(self, raw_content: str, compact_prompt: str, **kwargs) -> str:
        return f"格式要求：{compact_prompt}\n\n原始內容：\n{raw_content}"

    def _parse_response(self, content: str):
        return content

