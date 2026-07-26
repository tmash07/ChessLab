from collections import Counter
from data.pgn import get_opening, get_headers_from_pgn
from models.game import Game

def count_openings(games: list[Game]) -> Counter[str | None]:
    counter = Counter()
    for game in games:
        counter[game.opening.opening_name] += 1
    return counter

def filter_games_by_opening(games: list[Game], opening_name: str) -> list[Game]:
    filtered_games = []
    for game in games:
        if game.opening.opening_name != opening_name:
            continue
        filtered_games.append(game)
    return filtered_games

