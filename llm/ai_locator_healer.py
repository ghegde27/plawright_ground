from core.logger import Logger
from llm.locator_generator import LocatorGenerator
from llm.prompts import LOCATOR_HEAL_PROMPT


class AILocatorHealer:

    def __init__(
            self,
            page,
            locator_generator: LocatorGenerator,
    ):
        self.page = page
        self.locator_generator = locator_generator
        self.log = Logger.get_logger(self.__class__.__name__)

    def heal(
            self,
            page_name: str,
            locator_name: str,
            original_definition,
    ):
        self.log.info(f"[AI-HEAL] Starting → {page_name}.{locator_name}")

        # 1. Accessibility snapshot
        accessibility_dump = self._get_accessibility_snapshot()
        self.log.info(
            f"[AI-HEAL] Accessibility snapshot collected → "
            f"length={len(accessibility_dump)}"
        )

        # 2. Format original locator
        locator_definition = (
            f"strategy={original_definition.strategy}\n"
            f"value={original_definition.value}\n"
            f"options={original_definition.options}"
        )

        # 3. Build prompt
        prompt = LOCATOR_HEAL_PROMPT.substitute(
            page_name=page_name,
            locator_name=locator_name,
            locator_definition=locator_definition,
            accessibility_dump=accessibility_dump,
        )
        self.log.info(f"[AI-HEAL] Prompt created → length={len(prompt)}")

        # 4. Generate LocatorDefinition
        definition = self.locator_generator.generate(prompt)
        self.log.info(
            f"[AI-HEAL] Generated → strategy={definition.strategy} | "
            f"value={definition.value}"
        )

        return definition

    def _get_accessibility_snapshot(self) -> str:
        snapshot = self.page.accessibility.snapshot(interesting_only=False)

        if not snapshot:
            raise RuntimeError("Accessibility snapshot is empty")

        return self._format_snapshot(snapshot)

    def _format_snapshot(self, node: dict, level: int = 0) -> str:
        lines = []
        indent = "  " * level

        role = node.get("role", "")
        name = node.get("name", "")

        if role or name:
            lines.append(f"{indent}- role={role} name={name}")

        for child in node.get("children", []):
            child_text = self._format_snapshot(child, level + 1)
            if child_text:
                lines.append(child_text)

        return "\n".join(lines)
