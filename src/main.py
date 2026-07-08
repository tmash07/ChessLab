from api.chesscom import get_all_user_games
from analysis.records import get_record
from analysis.openings import top_10_openings

def get_player_analysis(username):
    games = get_all_user_games(username)
    
    print(f"Total games analyzed: {len(games)}\n")

    record = get_record(username, games)

    print(f"Wins: {record['wins']}\n Draws: {record['draws']}\n Losses: {record['losses']}\n")

    print("10 most common openings:")
    top_10_openings(games)

