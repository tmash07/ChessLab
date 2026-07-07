import requests
import chess.pgn
import io
from collections import Counter

headers = {
    "User-Agent": "ChessLab (contact: tmashqbeh@gmail.com)"
}
win_codes = ["win"]
draw_codes = ["agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"]
loss_codes = ["checkmated", "timeout", "resigned", "lose", "abandoned", "kingofthehill", "threecheck", "bughousepartnerlose"]

def api_error(code):
    print(f"Error accessing API. Status code: {code}")

def get_player_info(username):
    url = "https://api.chess.com/pub/player/" + username + "/stats"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        api_error(response.status_code)

def get_game_history(username, basetime, increment):
    url = "https://api.chess.com/pub/player/" + username + f"/games/live/{basetime}/{increment}"
    response=requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        api_error(response.status_code)

def get_player_archives(username):
    archives_url = "https://api.chess.com/pub/player/" + username + "/games/archives"
    archives_response = requests.get(archives_url, headers=headers)
    if archives_response.status_code != 200:
        api_error(archives_response.status_code)
        return
    return archives_response.json()["archives"]

def get_all_user_games(username):
    archives = get_player_archives(username)
    games_list = []
    for link in archives:
        response = requests.get(link, headers=headers)
        if response.status_code != 200:
            api_error(response.status_code)
            continue
        games_list.extend(response.json()["games"])
    return games_list
    

def get_record(username, games_list):
    wins = 0
    draws = 0
    losses = 0
    for game in games_list:
        color = "white" if game["white"]["username"] == username else "black"
        result = game[color]["result"]
        if (result in win_codes):
            wins += 1
        elif (result in draw_codes):
            draws += 1
        elif (result in loss_codes):
            losses += 1
        else:
            print("Error: result code not recognized")
    return wins, draws, losses

def extract_opening_from_pgn(pgn_string):
    if not pgn_string or not isinstance(pgn_string, str):
        return "Unknown"
    
    pgn_file = io.StringIO(pgn_string)
    headers = chess.pgn.read_headers(pgn_file)

    if headers is None:
        return "Unknown"
    
    eco = headers.get("ECO", "Unknown")
    return eco

def top_10_openings(games_list):
    counter = Counter()
    for game in games_list:
        pgn = game.get("pgn")
        counter[extract_opening_from_pgn(pgn)] += 1

    for opening, count in counter.most_common()[:10]:
        print(f"{opening}: {count}")


def get_player_analysis(username):
    games = get_all_user_games(username)
    
    print(f"Total games analyzed: {len(games)}\n")

    wins, draws, losses = get_record(username, games)

    print(f"Wins: {wins}\n Draws: {draws}\n Losses: {losses}\n")

    print("10 most common openings:")
    top_10_openings(games)

get_player_analysis("magnuscarlsen")