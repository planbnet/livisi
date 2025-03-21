from dataclasses import dataclass
from typing import Optional


@dataclass
class LivisiEvent:
    namespace: str
    properties: Optional[dict]
    source: str
    onState: Optional[bool]
    vrccData: Optional[float]
    luminance: Optional[int]
    isReachable: Optional[bool]
    sequenceNumber: Optional[str]
    type: Optional[str]
    timestamp: Optional[str]
    isOpen: Optional[bool]
    keyIndex: Optional[int]
    isLongKeyPress: Optional[bool]
