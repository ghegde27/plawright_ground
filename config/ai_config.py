"""AI/LLM runtime configuration.

Provider selection is feature-flag driven. Set AI_PROVIDER=claude to use
Anthropic Claude; otherwise the existing provider selected by LLM_PROVIDER
(or GROQ by default) is used.
"""

import os
from dataclasses import dataclass

from llm.models import DEFAULT_MODEL, ModelConfig
from llm.provider import Provider


_TRUE = {"1", "true", "yes", "on", "y"}


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in _TRUE


@dataclass(frozen=True)
class AIConfig:
    enabled: bool = True
    provider: Provider = Provider.GROQ
    model: ModelConfig = DEFAULT_MODEL
    locator_generation_enabled: bool = True
    locator_healing_enabled: bool = True
    test_generation_enabled: bool = True
    failure_analysis_enabled: bool = True

    @classmethod
    def from_env(cls) -> "AIConfig":
        """Build runtime configuration from environment variables.

        AI_PROVIDER=claude explicitly selects Claude. If it is not set,
        LLM_PROVIDER is used, preserving the existing framework behavior.
        """
        raw_provider = (
            os.getenv("AI_PROVIDER")
            or os.getenv("LLM_PROVIDER")
            or Provider.GROQ.value
        ).strip().lower()

        try:
            provider = Provider(raw_provider)
        except ValueError as exc:
            supported = ", ".join(p.value for p in Provider)
            raise ValueError(
                f"Unsupported AI_PROVIDER/LLM_PROVIDER '{raw_provider}'. "
                f"Supported providers: {supported}"
            ) from exc

        model_name = os.getenv("AI_MODEL") or os.getenv("LLM_MODEL")
        if model_name:
            model = ModelConfig(
                model=model_name,
                temperature=float(os.getenv("AI_TEMPERATURE", "0")),
                top_p=float(os.getenv("AI_TOP_P", "0.95")),
                max_completion_tokens=int(
                    os.getenv("AI_MAX_TOKENS", str(DEFAULT_MODEL.max_completion_tokens))
                ),
            )
        elif provider == Provider.CLAUDE:
            model = ModelConfig(
                model="claude-sonnet-5",
                max_completion_tokens=int(
                    os.getenv("AI_MAX_TOKENS", "4096")
                ),
            )
        else:
            model = DEFAULT_MODEL

        return cls(
            enabled=_bool_env("AI_ENABLED", True),
            provider=provider,
            model=model,
            locator_generation_enabled=_bool_env(
                "AI_LOCATOR_GENERATION", True
            ),
            locator_healing_enabled=_bool_env("AI_LOCATOR_HEALING", True),
            test_generation_enabled=_bool_env("AI_TEST_GENERATION", True),
            failure_analysis_enabled=_bool_env("AI_FAILURE_ANALYSIS", True),
        )
