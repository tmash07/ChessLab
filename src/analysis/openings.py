from collections import Counter
from data.pgn import get_opening, get_headers_from_pgn
from models.game import Game

def count_openings(games_list: list[Game]) -> Counter[str | None]:
    counter = Counter()
    for game in games_list:
        counter[game.eco] += 1
    return counter
