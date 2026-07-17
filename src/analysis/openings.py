from collections import Counter
from data.pgn import get_opening, get_headers_from_pgn
from models.game import Game

def count_openings(games_list: list[Game]) -> Counter[str | None]:
    counter = Counter()
    for game in games_list:
        if game.rules != "chess":
            continue
        counter[game.eco] += 1
    return counter

def filter_games_by_opening(games_list: list[Game], eco: str) -> list[Game]:
    filtered_games = []
    for game in games_list:
        if game.rules != "chess":
            continue
        if game.eco != eco:
            continue
        filtered_games.append(game)
    return filtered_games

# Not Complete
def count_opening_wins(username: str, games_list: list[Game]) -> Counter[str | None]:
    counter = Counter()
    for game in games_list:
        if game.rules != "chess":
            continue
        color = game.get_user_color(username)
        if color is None:
            continue
        if getattr(game, color).result is "win":
            counter[game.eco] += 1
    return counter
