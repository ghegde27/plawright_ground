from dataclasses import dataclass
from enum import Enum


class SupportedModel(str, Enum):
    DEEPSEEK_FLASH = "deepseek-ai/deepseek-v4-flash"
    GPT_5_5 = "gpt-5.5"
    CLAUDE_SONNET = "claude-sonnet-4"
    GEMINI_PRO = "gemini-2.5-pro"


@dataclass(frozen=True)
class ModelConfig:

    model: str
    temperature: float = 0
    top_p: float = 0.95
    max_tokens: int = 512

    # Optional vendor-specific settings
    reasoning: bool = True
    reasoning_effort: str = "high"


DEFAULT_MODEL = ModelConfig(
    model=SupportedModel.DEEPSEEK_FLASH.value,
    temperature=0,
    top_p=0.95,
    max_tokens=512,
)