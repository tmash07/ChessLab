import chess.pgn
import io
from datetime import datetime
from models.enums import Color
import re

type Headers = chess.pgn.Headers

def get_headers_from_pgn(pgn_string: str) -> Headers | None:
    pgn_file = io.StringIO(pgn_string)
    headers = chess.pgn.read_headers(pgn_file)
    return headers

def get_ratings(headers: Headers) -> dict[Color, int | None]:
    white_elo_raw = headers.get("WhiteElo", None)
    if white_elo_raw is not None and str.isdigit(white_elo_raw):
        white_elo = int(white_elo_raw)
    else: 
        white_elo = None
    black_elo_raw = headers.get("BlackElo", None)
    if black_elo_raw is not None and str.isdigit(black_elo_raw):
        black_elo = int(black_elo_raw)
    else: 
        black_elo = None
    return {Color.WHITE: white_elo, Color.BLACK: black_elo}

def get_users(headers: Headers) -> dict[Color, str | None]:
    white_user = headers.get("White")
    black_user = headers.get("Black")
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
    if not re.fullmatch(r"\d{4}\.\d{2}\.\d{2}", date):
        return None
    if not re.fullmatch(r"\d{2}:\d{2}:\d{2}", time):
        return None
    return datetime.strptime(date + " " + time, "%Y.%m.%d %H:%M:%S")
