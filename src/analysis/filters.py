from models.game import Game
from models.enums import Color, TimeClass
from datetime import datetime
from collections import defaultdict
from typing import Callable, Any

def filter_games(games: list[Game], predicate: Callable[[Any], bool]):
    return [game for game in games if predicate(game)]

def filter_by_user(user: str, games: list[Game]) -> list[Game]:
    return filter_games(games, lambda game: game.get_user_player(user) is not None)

def filter_by_color(user: str, games: list[Game], color: Color) -> list[Game]:
    return filter_games(games, lambda game: game.get_user_color(user) == color)

def filter_by_time_class(games: list[Game], time_class: TimeClass) -> list[Game]:
    return filter_games(games, lambda game: game.time_class == time_class)

def filter_by_time_control(games: list[Game], basetime: int, increment: int) -> list[Game]:
    return filter_games(games, lambda game: game.basetime == basetime and game.increment == increment)

def filter_by_opening_name(games: list[Game], opening: str) -> list[Game]:
    return filter_games(games, lambda game: game.opening.opening_name == opening)

def filter_by_date_range(games: list[Game], start: datetime, end: datetime) -> list[Game]:
    return filter_games(games, lambda game: start <= game.played_at < end)

def group_by_opening_name(games: list[Game]) -> dict[str, list[Game]]:
    groups = defaultdict(list)
    for game in games:
        groups[game.opening.opening_name].append(game)
    return dict(groups)

def group_by_opening_name_and_color(user: str, games: list[Game]) -> dict[tuple[str, Color], list[Game]]:
    groups = defaultdict(list)
    for game in games:
        color = game.get_user_color(user)
        if color is None:
            continue
        groups[game.opening.opening_name, color].append(game)
    return dict(groups)
