from enum import Enum


class Provider(str, Enum):
    OPENAI = "openai"
    GROQ = "groq"
    NVIDIA = "nvidia"
