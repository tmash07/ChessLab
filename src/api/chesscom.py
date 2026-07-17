import requests
from typing import Any

headers = {
    "User-Agent": "ChessLab (contact: tmashqbeh@gmail.com)"
}

JsonDict = dict[str, Any]

def api_error(code: int) -> None:
    print(f"Error accessing API. Status code: {code}")

def get_player_info(username: str) -> JsonDict | None:
    url = "https://api.chess.com/pub/player/" + username + "/stats"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        api_error(response.status_code)

def get_time_control_history(username: str, basetime: str, increment: str) -> list[JsonDict] | None:
    url = "https://api.chess.com/pub/player/" + username + f"/games/live/{basetime}/{increment}"
    response=requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        api_error(response.status_code)
        return None

def get_player_archives(username: str) -> list[str] | None:
    archives_url = "https://api.chess.com/pub/player/" + username + "/games/archives"
    archives_response = requests.get(archives_url, headers=headers)
    if archives_response.status_code != 200:
        api_error(archives_response.status_code)
        return None
    return archives_response.json()["archives"]

def get_all_user_games(username: str) -> list[JsonDict] | None:
    archives = get_player_archives(username)

    if archives is None:
        print("Archives list not found")
        return
    
    games_list = []
    for link in archives:
        response = requests.get(link, headers=headers)
        if response.status_code != 200:
            api_error(response.status_code)
            continue
        games_list.extend(response.json()["games"])
    return games_list

def get_monthly_user_games(username: str, year: str, month: str) -> list[JsonDict] | None:
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        api_error(response.status_code)
        return None
    return response.json()
