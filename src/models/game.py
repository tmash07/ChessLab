from dataclasses import dataclass
from datetime import datetime

@dataclass
class GamePlayer:
    username: str
    rating: int | None
    result: str | None
    accuracy: float | None

@dataclass
class Game:
    white: GamePlayer
    black: GamePlayer
    played_at: datetime
    basetime: int
    increment: int
    eco: str | None
    url: str
    raw_pgn: str
    rules: str
    rated: bool

    def get_user_color(self, user: str) -> str | None:
        if user.lower() == self.white.username.lower():
            return "white"
        if user.lower() == self.black.username.lower():
            return "black"
        return None