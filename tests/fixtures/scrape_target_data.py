from models.scrape_target import ScrapeTarget
from models.enums import ScrapeTargetType
from datetime import datetime, timezone

MONTHLY_SCRAPE_TARGET_1 = ScrapeTarget(
    username="atefplays",
    target_type=ScrapeTargetType.MONTHLY,
    year=2023,
    month=4,
    basetime=None,
    increment=None,
    last_successful_at=datetime(2026, 6, 1, tzinfo=timezone.utc),
    is_complete=True
)

TIME_CONTROL_SCRAPE_TARGET_1 = ScrapeTarget(
    username="hikaru",
    target_type=ScrapeTargetType.TIME_CONTROL,
    year=None,
    month=None,
    basetime=180,
    increment=2,
    last_successful_at=datetime(2026, 6, 1, tzinfo=timezone.utc),
    is_complete=False
)
