import pytest

from config.ai_config import AIConfig
from llm.provider import Provider


def test_defaults_to_existing_provider(monkeypatch):
    monkeypatch.delenv("AI_PROVIDER", raising=False)
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    config = AIConfig.from_env()

    assert config.provider == Provider.GROQ


def test_claude_is_selected_by_feature_flag(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "claude")

    config = AIConfig.from_env()

    assert config.provider == Provider.CLAUDE


def test_feature_flags_can_disable_healing(monkeypatch):
    monkeypatch.setenv("AI_LOCATOR_HEALING", "false")

    config = AIConfig.from_env()

    assert config.locator_healing_enabled is False


def test_invalid_provider_fails_fast(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "not-a-provider")

    with pytest.raises(ValueError, match="Unsupported AI_PROVIDER"):
        AIConfig.from_env()
