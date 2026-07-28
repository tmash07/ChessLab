from dataclasses import dataclass
from models.enums import GameResult

@dataclass
class Record:
    wins: int = 0
    draws: int = 0
    losses: int = 0
    
    @property
    def total_games(self) -> int:
        return self.wins + self.draws + self.losses
    
    @property
    def score(self) -> float:
        return self.wins + (0.5 * self.draws)
    
    @property
    def score_percentage(self) -> float | None:
        if self.total_games == 0:
            return None
        return self.score / self.total_games
    
    def add_result(self, result: GameResult) -> None:
        match result:
            case GameResult.WIN:
                self.wins += 1
                return
            case GameResult.DRAW:
                self.draws += 1
                return
            case GameResult.LOSS:
                self.losses += 1
                return
        raise ValueError("Game result not recognized")
    
@dataclass
class NumericSummary:
    minimum: float | None = None
    maximum: float | None = None
    count: int = 0
    missing: int = 0
    average: float | None = None
    total: float = 0

    def add_entry(self, entry: float | None) -> None:
        self.count += 1
        if entry is None:
            self.missing += 1
        else:
            self.minimum = entry if self.minimum is None else min(self.minimum, entry)
            self.maximum = entry if self.maximum is None else max(self.maximum, entry)
            self.total += entry
            self.average = self.total / (self.count - self.missing)

