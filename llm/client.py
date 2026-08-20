from core.logger import Logger

from llm.provider import Provider

from llm.providers.groq_provider import GroqProvider
from llm.providers.nvidia_provider import NvidiaProvider
from llm.providers.openai_provider import OpenAIProvider


class LLMClient:

    def __init__(
            self,
            provider,
            api_key,
            model_config,
            base_url=None,
    ):

        self.log = Logger.get_logger(
            self.__class__.__name__
        )

        self.provider_name = provider
        self.model_config = model_config

        self.log.info(
            f"[LLM] Initializing → "
            f"provider={provider}"
        )

        if provider == Provider.GROQ:

            self.provider = GroqProvider(
                api_key,
                model_config,
            )

        elif provider == Provider.OPENAI:

            self.provider = OpenAIProvider(
                api_key,
                base_url,
                model_config,
            )

        elif provider == Provider.NVIDIA:

            self.provider = NvidiaProvider(
                api_key,
                base_url,
                model_config,
            )

        else:

            self.log.error(
                f"[LLM] Unsupported provider → "
                f"{provider}"
            )

            raise ValueError(
                f"Unsupported provider: {provider}"
            )

        self.log.info(
            f"[LLM] Initialized → "
            f"provider={provider}"
        )

    # ==========================================================
    # CHAT
    # ==========================================================

    def chat(
            self,
            **kwargs,
    ):

        user_prompt = kwargs.get(
            "user_prompt"
        )

        system_prompt = kwargs.get(
            "system_prompt"
        )

        response_as_json = kwargs.get(
            "response_as_json",
            False,
        )

        # ------------------------------------------------------
        # Request information
        # ------------------------------------------------------

        self.log.info(
            f"[LLM] Request started → "
            f"provider={self.provider_name}"
        )

        if system_prompt:
            self.log.debug(
                f"[LLM] System prompt provided → "
                f"length={len(system_prompt)}"
            )

        if user_prompt:
            self.log.debug(
                f"[LLM] User prompt provided → "
                f"length={len(user_prompt)}"
            )

        self.log.debug(
            f"[LLM] Response format → "
            f"json={response_as_json}"
        )

        # ------------------------------------------------------
        # Call provider
        # ------------------------------------------------------

        try:

            result = self.provider.chat(
                **kwargs
            )

            # --------------------------------------------------
            # Response logging
            # --------------------------------------------------

            if isinstance(
                    result,
                    dict,
            ):

                self.log.info(
                    f"[LLM] Request successful → "
                    f"provider={self.provider_name} | "
                    f"response_keys="
                    f"{list(result.keys())}"
                )

            else:

                self.log.info(
                    f"[LLM] Request successful → "
                    f"provider={self.provider_name}"
                )

            return result

        except Exception as error:

            self.log.error(
                f"[LLM] Request failed → "
                f"provider={self.provider_name} | "
                f"error={error}"
            )

            raise
