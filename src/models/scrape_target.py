from dataclasses import dataclass
from datetime import datetime

@dataclass
class ScrapeTarget:
    username: str
    target_type: str
    year: int | None
    month: int | None
    basetime: int | None
    increment: int | None
    last_successful_at: datetime
    is_complete: bool