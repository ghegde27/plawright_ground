from abc import ABC, abstractmethod
from typing import Optional


class BaseLLMProvider(ABC):

    @abstractmethod
    def chat(
            self,
            user_prompt: str,
            system_prompt: Optional[str] = None,
            response_as_json: bool = False,
    ):
        pass
