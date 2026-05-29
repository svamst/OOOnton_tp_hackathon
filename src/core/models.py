from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Email:
    msg_id: str
    headers: dict = field(default_factory=dict)

    date: datetime
    sender: str
    subect: str = ""
    body: str = ""

    labels: Set[str] = field(default_factory=set)