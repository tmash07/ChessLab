from collections import Counter
from data.pgn import extract_opening_from_pgn

def top_10_openings(games_list):
    counter = Counter()
    for game in games_list:
        pgn = game.get("pgn")
        counter[extract_opening_from_pgn(pgn)] += 1

    for opening, count in counter.most_common()[:10]:
        print(f"{opening}: {count}")
