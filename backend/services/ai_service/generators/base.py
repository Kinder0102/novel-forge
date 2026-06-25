from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from config import MOCK_AI, SERVER_PORT
from models.novel import Novel
from models.chapter import ChapterContent
from models.outline import Outline, ChapterTitle
from models.worldbuilding import Worldbuilding
from models.character import Character
from models.scene import Scene
from services.ai_service.core import _get_module_config, _call_ai, schema_to_prompt


class BaseGenerator(ABC):
    module_name: str
    temperature: float = 0.8

    def __init__(self, db: Session):
        self.db = db

    async def generate(self, **kwargs):
        cfg = await _get_module_config(self.db, self.module_name)
        messages = self._build_messages(cfg, **kwargs)

        if MOCK_AI:
            content = await _call_ai(
                self.db, self.module_name, messages,
                api_key="",
                base_url=f"http://localhost:{SERVER_PORT}/mock",
                model=f"mock-{self.module_name}",
                temperature=self.temperature,
            )
        else:
            content = await _call_ai(
                self.db, self.module_name, messages,
                cfg["api_key"], cfg["base_url"], cfg["model"],
                temperature=self.temperature,
            )
        return self._parse_response(content)

    def _build_messages(self, cfg: dict, **kwargs) -> list[dict]:
        parts = []

        user_prompt = cfg.get("user_prompt", "")
        if user_prompt:
            parts.append(user_prompt)

        parts.append(self._build_fixed_instructions(**kwargs))
        parts.append(schema_to_prompt(self._get_output_schema()))
        parts.append(self._build_user_input(**kwargs))
        additional = self._build_additional_context(**kwargs)
        if additional:
            parts.append(additional)

        user_content = "\n\n".join(p for p in parts if p)
        return [
            {"role": "system", "content": cfg.get("system_prompt", "")},
            {"role": "user", "content": user_content},
        ]

    def _get_output_schema(self) -> dict:
        option = getattr(self, "OPTION", {}) or {}
        return option.get("outputSchema", {})

    def _fetch_worldbuilding(self, **kwargs) -> str:
        worldbuilding_id = kwargs.get("worldbuilding_id")
        if not worldbuilding_id:
            return ""
        record = self.db.query(Worldbuilding).filter(Worldbuilding.id == worldbuilding_id).first()
        return record.summary if record else ""

    def _fetch_character(self, **kwargs) -> str:
        character_ids = kwargs.get("character_ids") or []
        if not character_ids:
            return ""
        records = self.db.query(Character).filter(Character.id.in_(character_ids)).all()
        return "\n".join(c.summary for c in records if c.summary)

    def _fetch_outline(self, **kwargs) -> str:
        outline_id = kwargs.get("outline_id")
        chapter_title_id = kwargs.get("chapter_title_id")
        if not outline_id:
            if not chapter_title_id:
                return ""
            chapter_title = self.db.query(ChapterTitle).filter(ChapterTitle.id == chapter_title_id).first()
            outline_id = chapter_title.outline_id

        outline = self.db.query(Outline).filter(Outline.id == outline_id).first()
        return outline.summary if outline else ""

    def _fetch_writing_style(self, **kwargs) -> str:
        novel_id = kwargs.get("novel_id")
        if not novel_id:
            return ""
        novel = self.db.query(Novel).filter(Novel.id == novel_id).first()
        return novel.writing_style if novel and novel.writing_style else ""

    def _fetch_previous_summary(self, **kwargs) -> str:
        chapter_title_id = kwargs.get("chapter_title_id")
        if not chapter_title_id:
            return ""
        current = self.db.query(ChapterTitle).filter(ChapterTitle.id == chapter_title_id).first()
        if not current:
            return ""
        prev_ct = (
            self.db.query(ChapterTitle)
            .filter(
                ChapterTitle.outline_id == current.outline_id,
                ChapterTitle.idx < current.idx,
            )
            .order_by(ChapterTitle.idx.desc())
            .first()
        )
        if not prev_ct:
            return ""
        prev_content = (
            self.db.query(ChapterContent)
            .filter(ChapterContent.chapter_title_id == prev_ct.id)
            .first()
        )
        return prev_content.summary if prev_content and prev_content.summary else ""

    def _fetch_scene(self, **kwargs) -> str:
        chapter_title_id = kwargs.get("chapter_title_id")
        if not chapter_title_id:
            return ""
        scenes = (
            self.db.query(Scene)
            .filter(Scene.chapter_title_id == chapter_title_id)
            .order_by(Scene.scene_number)
            .all()
        )
        return "\n".join(s.summary for s in scenes if s.summary)

    def _build_additional_context(self, **kwargs) -> str:
        option = getattr(self, "OPTION", {}) or {}
        items = option.get("additional", [])
        lines = []
        for item in items:
            key = item.get("key", "")
            value = item.get("value", "")
            fetcher = getattr(self, f"_fetch_{key}", None)
            if fetcher:
                text = fetcher(**kwargs)
            else:
                text = kwargs.get(key, "")
            if text:
                lines.append(f"{value}：{text}")
        return "\n".join(lines)

    @abstractmethod
    def _build_fixed_instructions(self, **kwargs) -> str:
        ...

    @abstractmethod
    def _build_user_input(self, **kwargs) -> str:
        ...

    @abstractmethod
    def _parse_response(self, content: str):
        ...

    @abstractmethod
    def _compact_prompt(self) -> str:
        ...

    async def compact(self, raw_output) -> str:
        from .compact import CompactGenerator
        return await CompactGenerator(self.db).generate(
            raw_content=str(raw_output),
            compact_prompt=self._compact_prompt(),
        )
