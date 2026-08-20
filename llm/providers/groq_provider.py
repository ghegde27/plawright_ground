import json

from groq import Groq

from .base import BaseLLMProvider


class GroqProvider(BaseLLMProvider):

    def __init__(self, api_key, model_config):
        self.client = Groq(api_key=api_key)
        self.model_config = model_config

    def chat(
            self,
            user_prompt,
            system_prompt=None,
            response_as_json=False,
    ):

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

        response = self.client.chat.completions.create(
            model=self.model_config.model,
            messages=messages,
            temperature=self.model_config.temperature,
            top_p=self.model_config.top_p,
            max_tokens=self.model_config.max_completion_tokens,
        )

        content = response.choices[0].message.content

        if response_as_json:
            return json.loads(content)

        return content
