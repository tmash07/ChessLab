from api.chesscom import JsonDict
from models.game import Game, GamePlayer
from data.pgn import (
    get_headers_from_pgn, 
    get_rating_information, 
    get_winner, 
    get_time_control, 
    get_opening
)
from typing import Any

def get_accuracies(game: JsonDict) -> dict[str, float | None] | None:
    return game.get("accuracies")

def get_url(game: JsonDict) -> str:
    return game["url"]

def get_game_info(game: JsonDict) -> dict[str, Any] | None:
    headers = get_headers_from_pgn(game["pgn"])
    if headers is None:
        print("Headers not found")
        return None
    return {
        "time_control": get_time_control(headers),
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
        date = rating_info["date"],
        time = rating_info["time"],
        time_control = game_info["time_control"],
        eco = game_info["eco"],
        url = None if game_info is None else game_info["url"],
        raw_pgn = game["pgn"],
        rules = rules,
        rated = rated
    )



