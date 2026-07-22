from api.chesscom import JsonDict
from models.game import Game, GamePlayer
from data.pgn import (
    get_headers_from_pgn, 
    get_rating_information, 
    get_time_control, 
    get_opening
)
from typing import Any
from api.chesscom import get_time_control_history, get_monthly_user_games


def get_accuracies(game: JsonDict) -> dict[str, float | None] | None:
    return game.get("accuracies")

def get_url(game: JsonDict) -> str:
    return game["url"]

def get_game_info(game: JsonDict) -> dict[str, Any] | None:
    headers = get_headers_from_pgn(game["pgn"])
    if headers is None:
        print("Headers not found")
        return None
    time_control = get_time_control(headers)
    if time_control is None:
        basetime = increment = None
    elif "+" in time_control:
        base_str, inc_str = time_control.split("+")
        basetime = int(base_str)
        increment = int(inc_str)
    else:
        basetime = int(time_control)
        increment = 0
    return {
        "basetime" : basetime,
        "increment": increment,
        "eco": get_opening(headers),
        "url": get_url(game)
    }

def get_results(game: JsonDict) -> dict[str, str | None]:
    return {"white_result": game["white"]["result"], "black_result": game["black"]["result"]}

def get_rules(game: JsonDict) -> str:
    return game["rules"]

def is_rated(game: JsonDict) -> bool:
    return game["rated"]

def build_game_from_chesscom(game: JsonDict) -> Game | None:
    if game.get("pgn", None) is None:
        return None
    headers = get_headers_from_pgn(game["pgn"])
    if headers is None:
        print("Headers not found")
        return None
    rating_info = get_rating_information(headers)
    results = get_results(game)
    accuracies = get_accuracies(game)
    game_info = get_game_info(game)
    if game_info is None:
        print("Game info not found")
        return None
    rules = get_rules(game)
    rated = is_rated(game)

    white_user = GamePlayer(
        username = rating_info["white"]["user"],
        rating = rating_info["white"]["rating"],
        result = results["white_result"],
        accuracy = None if accuracies is None else accuracies["white"]
    )
    black_user = GamePlayer(
        username = rating_info["black"]["user"],
        rating = rating_info["black"]["rating"],
        result = results["black_result"],
        accuracy = None if accuracies is None else accuracies["black"]
    )
    return Game(
        white = white_user,
        black = black_user,
        played_at = rating_info["datetime"],
        basetime = game_info["basetime"],
        increment = game_info["increment"],
        eco = game_info["eco"],
        url = None if game_info is None else game_info["url"],
        raw_pgn = game["pgn"],
        rules = rules,
        rated = rated
    )

def build_gamelist_from_chesscom(raw_gamelist: list[JsonDict]) -> list[Game] | None:
    games = []
    for raw_game in raw_gamelist:
        game = build_game_from_chesscom(raw_game)
        if game is None:
            continue
        if game.rules != "chess":
            continue
        games.append(game)
    return games

def build_time_control_gamelist(username: str, basetime: str, increment: str) -> list[Game] | None:
    raw_gamelist = get_time_control_history(username, basetime, increment)
    if raw_gamelist is None:
        return None
    gamelist = build_gamelist_from_chesscom(raw_gamelist)
    return gamelist

def build_monthly_gamelist(username: str, year: str, month: str):
    raw_gamelist = get_monthly_user_games(username, year, month)
    if raw_gamelist is None:
        return None
    gamelist = build_gamelist_from_chesscom(raw_gamelist)
    return gamelist

        


