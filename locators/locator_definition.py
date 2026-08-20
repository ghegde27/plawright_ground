from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LocatorDefinition:
    name: str
    strategy: str
    value: str
    options: dict[str, Any] = field(
        default_factory=dict
    )
    description: str | None = None
