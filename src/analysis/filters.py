from models.game import Game
from models.enums import Color, TimeClass
from datetime import datetime
from collections import defaultdict

def filter_by_user(user: str, games: list[Game]) -> list[Game]:
    filtered_games = []
    for game in games:
        player = game.get_user_player(user)
        if player is not None:
            filtered_games.append(game)
    return filtered_games

def filter_by_color(user: str, games: list[Game], color: Color) -> list[Game]:
    filtered_games = []
    for game in games:
        game_color = game.get_user_color(user)
        if game_color == color:
            filtered_games.append(game)
    return filtered_games

def filter_by_time_class(games: list[Game], time_class: TimeClass) -> list[Game]:
    filtered_games = []
    for game in games:
        if game.time_class == time_class:
            filtered_games.append(game)
    return filtered_games

def filter_by_time_control(games: list[Game], basetime: int, increment: int) -> list[Game]:
    filtered_games = []
    for game in games:
        if game.basetime == basetime and game.increment == increment:
            filtered_games.append(game)
    return filtered_games

def filter_by_opening_name(games: list[Game], opening: str) -> list[Game]:
    filtered_games = []
    for game in games:
        if game.opening.opening_name == opening:
            filtered_games.append(game)
    return filtered_games

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

def filter_by_date_range(games: list[Game], start: datetime, end: datetime) -> list[Game]:
    filtered_games = []
    for game in games:
        if start <= game.played_at < end:
            filtered_games.append(game)
    return filtered_games