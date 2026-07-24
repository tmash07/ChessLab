from dataclasses import dataclass
from datetime import datetime
from models.enums import ScrapeTargetType

@dataclass
class ScrapeTarget:
    username: str
    target_type: ScrapeTargetType
    year: int | None
    month: int | None
    basetime: int | None
    increment: int | None
    last_successful_at: datetime
    is_complete: bool