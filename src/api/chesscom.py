import requests

headers = {
    "User-Agent": "ChessLab (contact: tmashqbeh@gmail.com)"
}

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
