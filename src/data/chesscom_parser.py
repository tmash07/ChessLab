from api.chesscom import JsonDict
from models.game import Game, GamePlayer
from data.pgn import (
    get_headers_from_pgn, 
    get_opening
)
from typing import Any
from api.chesscom import get_time_control_history, get_monthly_user_games
from models.enums import TimeClass
from datetime import datetime, timezone

def get_basetime_increment(game: JsonDict) -> dict[str, int]:
    time_control = game["time_control"]
    if "+" in time_control:
        base_str, inc_str = time_control.split("+")
        basetime = int(base_str)
        increment = int(inc_str)
    else:
        basetime = int(time_control)
        increment = 0
    return {"basetime" : basetime, "increment": increment}
    
def build_game_from_chesscom(game: JsonDict) -> Game | None:
    # TODO: Log these missing info skips
    if game is None:
        return None
    if game["rules"] != "chess" or game["time_class"] not in ["bullet", "blitz", "rapid"]:
        return None
    pgn = game.get("pgn", None)
    if pgn is None:
        return None
    headers = get_headers_from_pgn(pgn)
    if headers is None:
        return None
    time_control = get_basetime_increment(game)
    accuracies = game.get("accuracies")
    white_user = GamePlayer(
        username = game["white"]["username"],
        rating = game["white"]["rating"],
        result = game["white"]["result"],
        accuracy = None if accuracies is None else accuracies["white"]
    )
    black_user = GamePlayer(
        username = game["black"]["username"],
        rating = game["black"]["rating"],
        result = game["black"]["result"],
        accuracy = None if accuracies is None else accuracies["black"]
    )
    return Game(
        white = white_user,
        black = black_user,
        played_at = datetime.fromtimestamp(game["end_time"], timezone.utc),
        time_class = TimeClass(game["time_class"]),
        basetime = time_control["basetime"],
        increment = time_control["increment"],
        eco = game.get("eco", None),
        url = game["url"],
        raw_pgn = game["pgn"],
        rules = game["rules"],
        rated = game["rated"]
    )

def build_gamelist_from_chesscom(raw_gamelist: list[JsonDict]) -> list[Game] | None:
    games = []
    for raw_game in raw_gamelist:
        game = build_game_from_chesscom(raw_game)
        if game is not None:
            games.append(game)
    return games

def build_time_control_gamelist(username: str, basetime: int, increment: int) -> list[Game] | None:
    raw_gamelist = get_time_control_history(username, basetime, increment)
    if raw_gamelist is None:
        return None
    gamelist = build_gamelist_from_chesscom(raw_gamelist)
    return gamelist

def build_monthly_gamelist(username: str, year: int, month: int):
    raw_gamelist = get_monthly_user_games(username, year, month)
    if raw_gamelist is None:
        return None
    gamelist = build_gamelist_from_chesscom(raw_gamelist)
    return gamelist

        


