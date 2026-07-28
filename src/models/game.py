from dataclasses import dataclass
from datetime import datetime
from models.enums import Color, TimeClass, GameResult

win_codes = ["win"]
draw_codes = ["agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"]
loss_codes = ["checkmated", "timeout", "resigned", "lose", "abandoned", "kingofthehill", "threecheck", "bughousepartnerlose"]

@dataclass
class GamePlayer:
    username: str
    rating: int
    result: str
    accuracy: float | None

@dataclass
class GameOpening:
    eco: str | None
    opening_name: str
    extended_moves: str | None

@dataclass
class Game:
    white: GamePlayer
    black: GamePlayer
    played_at: datetime
    time_class: TimeClass
    basetime: int
    increment: int
    opening: GameOpening
    url: str
    raw_pgn: str
    rules: str
    rated: bool

    def get_player_by_color(self, color: Color) -> GamePlayer:
        if color == Color.WHITE:
            return self.white
        elif color == Color.BLACK:
            return self.black
        raise ValueError("Color not recognized")

    def get_user_color(self, user: str) -> Color | None:
        if user.lower() == self.white.username.lower():
            return Color.WHITE
        if user.lower() == self.black.username.lower():
            return Color.BLACK
        return None
    
    def get_opponent_color(self, user: str) -> Color | None:
        user_color = self.get_user_color(user)
        if user_color == Color.WHITE:
            return Color.BLACK
        if user_color == Color.BLACK:
            return Color.WHITE
        return None
    
    def get_user_player(self, user: str) -> GamePlayer | None:
        color = self.get_user_color(user)
        if color is None:
            return None
        return self.get_player_by_color(color)

    def get_opponent_player(self, user: str) -> GamePlayer | None:
        opponent_color = self.get_opponent_color(user)
        if opponent_color is None:
            return None
        return self.get_player_by_color(opponent_color)
    
    def get_user_result(self, user: str) -> GameResult | None:
        player = self.get_user_player(user)

        if player is None:
            return None
        if player.result in win_codes:
            return GameResult.WIN
        elif player.result in draw_codes:
            return GameResult.DRAW
        elif player.result in loss_codes:
            return GameResult.LOSS
        raise ValueError("Result code not recognized")
    
    def get_opponent_result(self, user: str) -> GameResult | None:
        opponent = self.get_opponent_player(user)

        if opponent is None:
            return None
        if opponent.result in win_codes:
            return GameResult.WIN
        elif opponent.result in draw_codes:
            return GameResult.DRAW
        elif opponent.result in loss_codes:
            return GameResult.LOSS
        raise ValueError("Result code not recognized")