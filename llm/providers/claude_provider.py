"""Anthropic Claude provider implementing the framework LLM contract."""

import json
from typing import Optional

from .base import BaseLLMProvider


class ClaudeProvider(BaseLLMProvider):
    """Claude adapter.

    The Anthropic SDK is imported lazily so existing non-Claude runs do not
    require the SDK to be imported at module load time.
    """

    def __init__(self, api_key: str, model_config):
        if not api_key:
            raise ValueError(
                "Anthropic API key is required when AI_PROVIDER=claude"
            )

        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise ImportError(
                "The 'anthropic' package is required for AI_PROVIDER=claude. "
                "Install project dependencies or run: pip install anthropic"
            ) from exc

        self.client = Anthropic(api_key=api_key)
        self.model_config = model_config

    def chat(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        response_as_json: bool = False,
        **kwargs,
    ):
        # Claude Sonnet 5 does not accept non-default sampling parameters.
        # Keep the common ModelConfig contract, but omit temperature/top_p
        # from the Anthropic request.
        request = {
            "model": self.model_config.model,
            "max_tokens": self.model_config.max_completion_tokens,
            "messages": [{"role": "user", "content": user_prompt}],
        }

        if system_prompt:
            request["system"] = system_prompt

        response = self.client.messages.create(**request)
        content = "".join(
            block.text
            for block in response.content
            if getattr(block, "type", None) == "text"
        ).strip()

        if response_as_json:
            return self._parse_json(content)

        return content

    @staticmethod
    def _parse_json(content: str):
        """Parse JSON while tolerating accidental markdown code fences."""
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`").strip()
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()
        return json.loads(cleaned)
