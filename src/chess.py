import requests
import time

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

def get_full_game_history(username):
    archives_url = "https://api.chess.com/pub/player/" + username + "/games/archives"
    archives_response = requests.get(archives_url, headers=headers)
    if archives_response.status_code != 200:
        api_error(archives_response.status_code)
        return
    archives = archives_response.json()["archives"]
    wins, draws, losses = 0, 0, 0
    for link in archives:
        response = requests.get(link, headers=headers)
        if response.status_code != 200:
            api_error(response.status_code)
            continue
        games_list = response.json()["games"]
        linkw, linkd, linkl = get_record(username, games_list)
        wins += linkw
        draws += linkd
        losses += linkl
    return wins, draws, losses
    

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

a, b, c = get_full_game_history("hikaru")
print(f"Wins:{a}\n Draws:{b}\n Losses:{c}")


    