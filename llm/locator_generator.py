import json
import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from mcp_server.models import DEFAULT_MODEL
from mcp_server.prompts import (
    SYSTEM_PROMPT,
    ACCESSIBILITY_PROMPT,
    HTML_PROMPT,
    COMBINED_PROMPT,
)

load_dotenv(verbose=True)

class LocatorGenerator:

    def __init__(
            self,
            api_key: str,
            base_url: str,
            model_config=DEFAULT_MODEL,
    ):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model_config = model_config

    # ------------------------------------------------------------------
    # Generic Chat Method
    # ------------------------------------------------------------------
    def chat(
            self,
            user_prompt: str,
            system_prompt: Optional[str] = None,
            response_as_json: bool = False,
    ):
        """
        Generic chat utility.

        Args:
            user_prompt: Prompt from the caller.
            system_prompt: Optional system prompt.
            response_as_json: Parse response as JSON.

        Returns:
            str | dict
        """

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        kwargs = {}

        if response_as_json:
            kwargs["response_format"] = {
                "type": "json_object"
            }

        response = self.client.chat.completions.create(
            model=self.model_config.model,
            messages=messages,
            temperature=self.model_config.temperature,
            top_p=self.model_config.top_p,
            max_tokens=self.model_config.max_tokens,
            **kwargs,
        )

        content = response.choices[0].message.content

        if response_as_json:
            return json.loads(content)

        return content

    # ------------------------------------------------------------------
    # Locator Specific
    # ------------------------------------------------------------------
    def _build_prompt(
            self,
            *,
            html: Optional[str] = None,
            accessibility_dump: Optional[str] = None,
    ) -> str:

        if html and accessibility_dump:
            return COMBINED_PROMPT.substitute(
                html=html,
                accessibility_dump=accessibility_dump,
            )

        if accessibility_dump:
            return ACCESSIBILITY_PROMPT.substitute(
                accessibility_dump=accessibility_dump,
            )

        if html:
            return HTML_PROMPT.substitute(html=html)

        raise ValueError(
            "Either html or accessibility_dump must be provided."
        )

    def generate_locator(
            self,
            *,
            html: Optional[str] = None,
            accessibility_dump: Optional[str] = None,
    ) -> str:

        prompt = self._build_prompt(
            html=html,
            accessibility_dump=accessibility_dump,
        )

        result = self.chat(
            user_prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            response_as_json=True,
        )

        return result.get("locator", "")



if __name__ == '__main__':
    client = LocatorGenerator(
        api_key=os.getenv("API_KEY", ""),
        base_url=os.getenv("BASE_URL", "")
    )

response = client.chat(
    user_prompt="Write a Python program to reverse a string."
)

print(response)