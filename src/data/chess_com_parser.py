from api.chesscom import JsonDict
from models.game import Game, GamePlayer
from data.pgn import (
    get_headers_from_pgn, 
    get_rating_information, 
    get_winner, 
    get_time_control, 
    get_opening
)

def get_accuracies(game: JsonDict) -> dict[str, float | None]:
    return game["accuracies"]

def get_url(game: JsonDict) -> str:
    return game["url"]

def get_game_info(game: JsonDict):
    headers = get_headers_from_pgn(game["pgn"])
    if headers is None:
        print("Headers not found")
        return None
    return {
        "time_control": get_time_control(headers),
        "eco": get_opening(headers),
        "url": get_url(game)
    }


def build_game_object(game: JsonDict) -> Game | None:
    headers = get_headers_from_pgn(game["pgn"])
    if headers is None:
        print("Headers not found")
        return None
    rating_info = get_rating_information(headers)
    result = get_winner(headers)
    match result:
        case "1-0":
            white_result = "win"
            black_result = "loss"
        case "1/2-1/2":
            white_result = black_result = "draw"
        case "0-1":
            white_result = "loss"
            black_result = "win"
        case _:
            white_result = None
            black_result = None
    accuracies = get_accuracies(game)
    game_info = get_game_info(game)
    if game_info is None:
        print("Game info not found")
        return None

    white_user = GamePlayer(
        username = rating_info["white"]["user"],
        rating = rating_info["white"]["rating"],
        result = white_result,
        color = "white",
        accuracy = accuracies["white"]
    )
    black_user = GamePlayer(
        username = rating_info["black"]["user"],
        rating = rating_info["black"]["rating"],
        result = black_result,
        color = "black",
        accuracy = accuracies["black"]
    )
    return Game(
        white = white_user,
        black = black_user,
        date = rating_info["date"],
        time = rating_info["time"],
        time_control = game_info["time_control"],
        eco = game_info["eco"],
        url = game_info["url"],
        raw_pgn = game["pgn"]
    )



