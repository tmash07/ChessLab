from enum import StrEnum

class Color(StrEnum):
    WHITE = "white"
    BLACK = "black"

class ScrapeTargetType(StrEnum):
    MONTHLY = "monthly"
    TIME_CONTROL = "time_control"

class TimeClass(StrEnum):
    BULLET = "bullet"
    BLITZ = "blitz"
    RAPID = "rapid"

class GameResult(StrEnum):
    WIN = "win"
    DRAW = "draw"
    LOSS = "loss"