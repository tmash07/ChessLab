from dataclasses import dataclass, fields
from models.enums import GameResult, Color, TimeClass

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

    def add_entry(self, entry: int | float | None) -> None:
        self.count += 1
        if entry is None:
            self.missing += 1
        else:
            self.minimum = entry if self.minimum is None else min(self.minimum, entry)
            self.maximum = entry if self.maximum is None else max(self.maximum, entry)
            self.total += entry
            self.average = self.total / (self.count - self.missing)

@dataclass(frozen=True)
class PerformanceReport:
    record: Record
    player_rating: NumericSummary
    opponent_rating: NumericSummary
    rating_difference: NumericSummary
    player_accuracy: NumericSummary
    opponent_accuracy: NumericSummary
    total_games: int

    def report_fields(self) -> dict:
        return {
        field.name: getattr(self, field.name)
        for field in fields(type(self))
        }

@dataclass(frozen=True)
class ColorReport(PerformanceReport):
    color: Color

@dataclass(frozen=True)
class TimeClassReport(PerformanceReport):
    time_class: TimeClass

@dataclass(frozen=True)
class OpeningReport(ColorReport):
    opening_name: str

@dataclass
class Report:
    username: str
    overall: PerformanceReport
    by_color: list[ColorReport]
    by_time_class: list[TimeClassReport]
    by_opening: list[OpeningReport]
    longest_win_streak: int
