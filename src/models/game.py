from dataclasses import dataclass
from datetime import datetime
from models.enums import Color, TimeClass

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
    time_class: TimeClass
    basetime: int
    increment: int
    eco: str | None
    url: str
    raw_pgn: str
    rules: str
    rated: bool

    def get_user_color(self, user: str) -> Color | None:
        if user.lower() == self.white.username.lower():
            return Color.WHITE
        if user.lower() == self.black.username.lower():
            return Color.BLACK
        return None
    
    def get_player_by_color(self, color: Color) -> GamePlayer:
        if color == Color.WHITE:
            return self.white
        elif color == Color.BLACK:
            return self.black