from typing import Any
from data.pgn import get_rating_information, get_headers_from_pgn

def get_user_rating(user: str, game: dict[str, Any]) -> int | None:
    headers = get_headers_from_pgn(game["pgn"])
    if headers is None:
        print("Headers not found")
        return None
    
    info = get_rating_information(headers)
    if info is None:
        print("Info not found")
        return None
    
    if info["white"]["user"] == user:
        return info["white"]["rating"]
    elif info["white"]["black"] == user:
        return info["black"]["rating"]
    else:
        print("User not found")
        return None