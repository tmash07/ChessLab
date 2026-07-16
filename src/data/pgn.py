import chess.pgn
import io
from typing import Any

type Headers = chess.pgn.Headers

def get_headers_from_pgn(pgn_string: str) -> Headers | None:
    if not pgn_string or not isinstance(pgn_string, str):
        return None
    
    pgn_file = io.StringIO(pgn_string)
    headers = chess.pgn.read_headers(pgn_file)
    return headers

def get_ratings(headers: Headers) -> dict[str, int | None]:
    white_elo_raw = headers.get("WhiteElo", None)
    white_elo = int(white_elo_raw) if white_elo_raw is not None else None
    black_elo_raw = headers.get("BlackElo", None)
    black_elo = int(black_elo_raw)if black_elo_raw is not None else None
    return {"white_elo": white_elo, "black_elo": black_elo}

def get_users(headers: Headers) -> dict[str, str | None]:
    white_user = headers.get("White", None)
    black_user = headers.get("Black", None)
    return {"white_user": white_user, "black_user": black_user}

def get_time_control(headers: Headers) -> str | None:
    return headers.get("TimeControl", None)

def get_user_color(username: str, headers: Headers) -> str | None:
    users = get_users(headers)

    if users["white_user"] == username: return "white"
    if users["black_user"] == username: return "black"
    return None

def get_opening(headers: Headers) -> str | None:
    return headers.get("ECO", None)

def get_date_and_time(headers: Headers) -> dict[str, str | None]:
    date = headers.get("UTCDate", None)
    time = headers.get("UTCTime", None)
    return {"date": date, "time": time}
    
def get_winner(headers: Headers) -> str | None:
    result = headers.get("Result", None)
    if result is None:
        print("No result found")
        return None
    if result == "0-1":
        return "black"
    elif result == "1-0":
        return "white"
    elif result == "1/2-1/2":
        return "draw"
    else:
        print("Result cannot be parsed")
        return None
    
def get_rating_information(headers: Headers) -> dict[str, Any]:
    users = get_users(headers)
    ratings = get_ratings(headers)
    date_and_time = get_date_and_time(headers)

    return {
        "white": {
            "user": users["white_user"],
            "rating": ratings["white_elo"]
        },
        "black": {
            "user": users["black_user"],
            "rating": ratings["black_elo"]
        },
        "date": date_and_time["date"],
        "time": date_and_time["time"]
    }
