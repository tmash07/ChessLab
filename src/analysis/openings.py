from collections import Counter
from data.pgn import get_opening, get_headers_from_pgn
from api.chesscom import JsonDict

def top_10_openings(games_list: list[JsonDict]) -> Counter[str | None]:
    counter = Counter()
    for game in games_list:
        pgn = game.get("pgn")
        if pgn is None:
            continue
        headers = get_headers_from_pgn(pgn)
        if headers is None:
            continue
        else:
            counter[get_opening(headers)] += 1

    return counter
