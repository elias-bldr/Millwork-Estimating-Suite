# models.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Part:
    item_type: str
    sku: str
    qty: float
    cost_each: float
    descr: str

@dataclass
class Assembly:
    name: str
    folder: str = "Misc"
    qty:    float = 1.0
    parts: List[Part] = field(default_factory=list)
