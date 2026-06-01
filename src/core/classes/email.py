from dataclasses import dataclass, field
from datetime import datetime
@dataclass
class Email:
    msg_id: str = ""
    headers: dict = field(default_factory=dict)

    sender: str = ""
    receiver: str = ""
    date: datetime = datetime.now()
    subject: str = ""
    body: str = ""

    attachments: set[str] = field(default_factory=set)

    tags: set[str] = field(default_factory=set)

