from core.logger import Logger
from llm.provider import Provider

class LLMClient:
    """Provider-neutral LLM facade used by all AI framework components."""

    def __init__(
        self,
        provider=None,
        api_key=None,
        model_config=None,
        base_url=None,
    ):
        self.log = Logger.get_logger(self.__class__.__name__)

        self.provider_name = Provider(provider) if provider else None
        self.model_config = model_config

        if self.provider_name is None:
            from config.ai_config import AIConfig

            config = AIConfig.from_env()
            self.provider_name = config.provider
            self.model_config = config.model
            api_key = api_key or self._api_key_for(config.provider)
            base_url = base_url or self._base_url_for(config.provider)

        self.model_config = self.model_config or self._default_model()
        api_key = api_key or self._api_key_for(self.provider_name)
        base_url = base_url or self._base_url_for(self.provider_name)

        self.log.info(
            f"[LLM] Initializing → provider={self.provider_name.value}"
        )

        if self.provider_name == Provider.GROQ:
            from llm.providers.groq_provider import GroqProvider
            self.provider = GroqProvider(api_key, self.model_config)
        elif self.provider_name == Provider.OPENAI:
            from llm.providers.openai_provider import OpenAIProvider
            self.provider = OpenAIProvider(api_key, base_url, self.model_config)
        elif self.provider_name == Provider.NVIDIA:
            from llm.providers.nvidia_provider import NvidiaProvider
            self.provider = NvidiaProvider(api_key, base_url, self.model_config)
        elif self.provider_name == Provider.CLAUDE:
            from llm.providers.claude_provider import ClaudeProvider
            self.provider = ClaudeProvider(api_key, self.model_config)
        else:
            raise ValueError(f"Unsupported provider: {self.provider_name}")

        self.log.info(
            f"[LLM] Initialized → provider={self.provider_name.value}"
        )

    @classmethod
    def from_env(cls):
        return cls()

    @staticmethod
    def _default_model():
        from llm.models import DEFAULT_MODEL

        return DEFAULT_MODEL

    @staticmethod
    def _api_key_for(provider: Provider):
        import os

        return {
            Provider.CLAUDE: os.getenv("ANTHROPIC_API_KEY"),
            Provider.OPENAI: os.getenv("OPENAI_API_KEY"),
            Provider.GROQ: os.getenv("GROQ_API_KEY"),
            Provider.NVIDIA: os.getenv("NVIDIA_API_KEY"),
        }.get(provider)

    @staticmethod
    def _base_url_for(provider: Provider):
        import os

        return {
            Provider.OPENAI: os.getenv("OPENAI_BASE_URL"),
            Provider.NVIDIA: os.getenv("NVIDIA_BASE_URL"),
        }.get(provider)

    def chat(self, **kwargs):
        user_prompt = kwargs.get("user_prompt")
        system_prompt = kwargs.get("system_prompt")
        response_as_json = kwargs.get("response_as_json", False)

        self.log.info(
            f"[LLM] Request started → provider={self.provider_name.value}"
        )
        if system_prompt:
            self.log.debug(
                f"[LLM] System prompt provided → length={len(system_prompt)}"
            )
        if user_prompt:
            self.log.debug(
                f"[LLM] User prompt provided → length={len(user_prompt)}"
            )
        self.log.debug(f"[LLM] Response format → json={response_as_json}")

        try:
            result = self.provider.chat(**kwargs)
            self.log.info(
                f"[LLM] Request successful → provider={self.provider_name.value}"
            )
            return result
        except Exception as error:
            self.log.error(
                f"[LLM] Request failed → provider={self.provider_name.value} | error={error}"
            )
            raise
