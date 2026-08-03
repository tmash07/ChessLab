from models.game import Game
from models.summary import Record, NumericSummary
from models.enums import GameResult
from collections import Counter
from collections.abc import Iterable
    
def get_record(user: str, games: list[Game]) -> Record:
    record = Record()
    for game in games:
        result = game.get_user_result(user)
        if result is not None:
            record.add_result(result)
    return record

def get_ratings(user: str, games: list[Game]) -> list[int]:
    ratings = []
    for game in games:
        player = game.get_user_player(user)
        if player is not None:
            ratings.append(player.rating)
    return ratings

def get_opponent_ratings(user: str, games: list[Game]) -> list[int]:
    ratings = []
    for game in games:
        opponent = game.get_opponent_player(user)
        if opponent is not None:
            ratings.append(opponent.rating)
    return ratings

def get_rating_differences(user: str, games: list[Game]) -> list[int]:
    differences = []
    for game in games:
        player = game.get_user_player(user)
        opponent = game.get_opponent_player(user)
        if player is not None and opponent is not None:
            differences.append(player.rating - opponent.rating)
    return differences

def get_accuracies(user: str, games: list[Game]) -> list[float | None]:
    accuracies = []
    for game in games:
        player = game.get_user_player(user)
        if player is not None:
            accuracies.append(player.accuracy)
    return accuracies

def get_opponent_accuracies(user: str, games: list[Game]) -> list[float | None]:
    accuracies = []
    for game in games:
        opponent = game.get_opponent_player(user)
        if opponent is not None:
            accuracies.append(opponent.accuracy)
    return accuracies

def find_longest_win_streak(user: str, games: list[Game]) -> int:
    streak = 0
    current = 0
    for game in games:
        result = game.get_user_result(user)
        if result is GameResult.WIN:
            current += 1
            streak = max(current, streak)
        elif result is not None:
            current = 0
    return streak

def build_numeric_summary(entries: Iterable[int | float | None]) -> NumericSummary:
    summary = NumericSummary()
    for entry in entries:
        summary.add_entry(entry)
    return summary

def count_openings(games: list[Game]) -> Counter[str]:
    counter = Counter()
    for game in games:
        counter[game.opening.opening_name] += 1
    return counter

def count_results(user: str, games: list[Game]) -> Counter[str]:
    counter = Counter()
    for game in games:
        player = game.get_user_player(user)
        if player is not None:
            counter[player.result] += 1
    return counter

def count_opponent_results(user: str, games: list[Game]) -> Counter[str]:
    counter = Counter()
    for game in games:
        opponent = game.get_opponent_player(user)
        if opponent is not None:
            counter[opponent.result] += 1
    return counter

