from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Email:
    file_name: str = ""
    subject: str = ""
    body: str = ""
    tags: dict = field(default_factory=dict)