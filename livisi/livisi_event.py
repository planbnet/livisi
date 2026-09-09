from dataclasses import dataclass


@dataclass
class LivisiEvent:
    namespace: str
    properties: dict | None
    source: str
    onState: bool | None
    vrccData: float | None
    luminance: int | None
    isReachable: bool | None
    sequenceNumber: str | None
    type: str | None
    timestamp: str | None
    isOpen: bool | None
    keyIndex: int | None
    isLongKeyPress: bool | None
