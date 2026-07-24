import chess.pgn
import io
from datetime import datetime
from models.enums import Color

type Headers = chess.pgn.Headers

def get_headers_from_pgn(pgn_string: str) -> Headers | None:
    pgn_file = io.StringIO(pgn_string)
    headers = chess.pgn.read_headers(pgn_file)
    return headers

def get_ratings(headers: Headers) -> dict[Color, int | None]:
    white_elo_raw = headers.get("WhiteElo", None)
    white_elo = int(white_elo_raw) if white_elo_raw is not None else None
    black_elo_raw = headers.get("BlackElo", None)
    black_elo = int(black_elo_raw)if black_elo_raw is not None else None
    return {Color.WHITE: white_elo, Color.BLACK: black_elo}

def get_users(headers: Headers) -> dict[Color, str]:
    white_user = headers["White"]
    black_user = headers["Black"]
    return {Color.WHITE: white_user, Color.BLACK: black_user}

def get_user_color(username: str, headers: Headers) -> Color | None:
    users = get_users(headers)
    if users[Color.WHITE] == username: return Color.WHITE
    if users[Color.BLACK] == username: return Color.BLACK
    return None

def get_opening(headers: Headers) -> str | None:
    return headers.get("ECO", None)

def get_date_and_time(headers: Headers) -> datetime | None:
    date = headers.get("UTCDate", None)
    time = headers.get("UTCTime", None)
    if date is None or time is None:
        return None
    return datetime.strptime(date + " " + time, "%Y.%m.%d %H:%M:%S")
