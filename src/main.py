from api.chesscom import get_all_user_games
from analysis.records import get_record
from analysis.openings import count_openings
from data.chesscom_parser import build_game_from_chesscom

def get_player_analysis(username: str) -> None:
    games_raw = get_all_user_games(username)
    if games_raw is None:
        return None
    games = []
    for game_raw in games_raw:
        game = build_game_from_chesscom(game_raw)
        if game is not None and game.rules == "chess": 
            games.append(game)
    
    print(f"Total games analyzed: {len(games)}\n")

    record = get_record(username, games)

    print(f"Wins: {record['wins']}\n Draws: {record['draws']}\n Losses: {record['losses']}\n")

    counter = count_openings(games)
    print("10 most common openings:")
    for opening, count in counter.most_common(10):
        print(f"{opening}: {count}")

get_player_analysis("fabianocaruana")
