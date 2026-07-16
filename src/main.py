from api.chesscom import get_all_user_games
from analysis.records import get_record
from analysis.openings import top_10_openings

def get_player_analysis(username: str) -> None:
    games = get_all_user_games(username)
    if games is None:
        return
    
    print(f"Total games analyzed: {len(games)}\n")

    record = get_record(username, games)

    print(f"Wins: {record['wins']}\n Draws: {record['draws']}\n Losses: {record['losses']}\n")

    counter = top_10_openings(games)
    print("10 most common openings:")
    for opening, count in counter.most_common(10):
        print(f"{opening}: {count}")

get_player_analysis("fabianocaruana")
