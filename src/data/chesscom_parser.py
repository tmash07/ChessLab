from models.game import Game, GamePlayer, GameOpening
from data.pgn import (
    get_headers_from_pgn, 
)
from integrations.chesscom import get_time_control_history, get_monthly_user_games, JsonDict
from models.enums import TimeClass
from datetime import datetime, timezone
import re

def get_basetime_increment(game: JsonDict) -> dict[str, int] | None:
    time_control = game.get("time_control")
    # Regex expression ensures time_control is in format "a+b" for numbers a and b
    if time_control is None or not str or not bool(re.fullmatch(r"\d+(\+\d+)?", time_control)):
        return None
    if "+" in time_control:
        base_str, inc_str = time_control.split("+")
        basetime = int(base_str)
        increment = int(inc_str)
    else:
        basetime = int(time_control)
        increment = 0
    return {"basetime" : basetime, "increment": increment}

def get_opening(game: JsonDict) -> GameOpening | None:
    url = game.get("eco")
    if url is None:
        return None
    opening = url.rsplit("/", 1)[-1]
    # Determine if opening starts with ECO code
    eco_partition = opening.partition("-")
    if bool(re.match(r"^[A-E][0-9]{2}$", eco_partition[0])):
        eco = eco_partition[0]
        opening = eco_partition[2]
    else:
        eco = None
    # Separate opening name and extended movelist
    split = re.search(r"\.\.\.|[0-9]\.", opening)
    if split:
        idx = split.start()
        opening_name = opening[:idx]
        extended_moves = opening[idx:]
    else:
        opening_name = opening
        extended_moves = None
    opening_name = opening_name.rstrip("-").replace("-", " ")
    return GameOpening(eco=eco, opening_name=opening_name, extended_moves=extended_moves)
    
def build_game_from_chesscom(game: JsonDict) -> Game | None:

    # TODO: Log these missing info skips
    if game is None:
        return None
    if game.get("rules") != "chess" or game.get("time_class") not in ["bullet", "blitz", "rapid"]:
        return None
    pgn = game.get("pgn", None)
    if pgn is None:
        return None
    headers = get_headers_from_pgn(pgn)
    if headers is None:
        return None
    try:
        time_control = get_basetime_increment(game)
        opening = get_opening(game)
        if time_control is None or opening is None:
            return None
        accuracies = game.get("accuracies")
        white_user = GamePlayer(
            username = game["white"]["username"].strip().lower(),
            rating = game["white"]["rating"],
            result = game["white"]["result"],
            accuracy = None if accuracies is None else accuracies["white"]
        )
        black_user = GamePlayer(
            username = game["black"]["username"].strip().lower(),
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
            opening = opening,
            url = game["url"],
            raw_pgn = game["pgn"],
            rules = game["rules"],
            rated = game["rated"]
        )
    except (KeyError, TypeError, ValueError) as e:
        # TODO: Log skipped game
        return None

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

        


