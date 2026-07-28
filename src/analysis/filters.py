from models.game import Game
from models.enums import Color, TimeClass
from datetime import datetime

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

def filter_by_date_range(games: list[Game], start: datetime, end: datetime) -> list[Game]:
    filtered_games = []
    for game in games:
        if start <= game.played_at <= end:
            filtered_games.append(game)
    return filtered_games