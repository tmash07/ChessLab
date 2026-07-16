import chess.pgn
import io

type Headers = chess.pgn.Headers

def get_headers_from_pgn(pgn_string: str) -> Headers | None:
    if not pgn_string or not isinstance(pgn_string, str):
        return None
    
    pgn_file = io.StringIO(pgn_string)
    headers = chess.pgn.read_headers(pgn_file)
    return headers

def get_pregame_ratings(headers: Headers) -> dict[str, int | None]:
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
    

