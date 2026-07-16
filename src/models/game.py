from dataclasses import dataclass

@dataclass
class GamePlayer:
    username: str
    rating: int
    result: str | None
    accuracy: float | None

@dataclass
class Game:
    white: GamePlayer
    black: GamePlayer
    date: str
    time: str
    time_control: str | None
    eco: str | None
    url: str | None
    raw_pgn: str
    rules: str
    rated: bool

    def get_user_color(self, user: str) -> str | None:
        if user.lower() == self.white.username.lower():
            return "white"
        if user.lower() == self.black.username.lower():
            return "black"
        return None