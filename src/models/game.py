from dataclasses import dataclass

@dataclass
class GamePlayer:
    username: str
    rating: int
    result: str | None
    color: str
    accuracy: float | None

@dataclass
class Game:
    white: GamePlayer
    black: GamePlayer
    date: str
    time: str
    time_control: str | None
    eco: str | None
    url: str
    raw_pgn: str