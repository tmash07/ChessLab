import requests
from typing import Any
from exceptions import ChessComApiError

headers = {
    "User-Agent": "ChessLab (contact: tmashqbeh@gmail.com)"
}

JsonDict = dict[str, Any]

def get_player_info(username: str) -> JsonDict:
    url = "https://api.chess.com/pub/player/" + username + "/stats"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise ChessComApiError(f"Could not find player info, API response code: {response.status_code}")

def get_time_control_history(username: str, basetime: int, increment: int) -> list[JsonDict] | None:
    url = "https://api.chess.com/pub/player/" + username + f"/games/live/{str(basetime)}/{str(increment)}"
    response=requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise ChessComApiError(f"Could not get time control history, API response code: {response.status_code}")

def get_player_archives(username: str) -> list[str] | None:
    archives_url = "https://api.chess.com/pub/player/" + username + "/games/archives"
    archives_response = requests.get(archives_url, headers=headers)
    if archives_response.status_code == 200:
        return archives_response.json()["archives"]
    else:
        raise ChessComApiError(f"Could not get player archives, API response code: {archives_response.status_code}")

def get_all_user_games(username: str) -> list[JsonDict] | None:
    archives = get_player_archives(username)

    if archives is None:
        print("Archives list not found")
        return
    
    games_list = []
    for link in archives:
        response = requests.get(link, headers=headers)
        if response.status_code != 200:
            # TODO: Log failed archives
            continue
        games_list.extend(response.json()["games"])
    return games_list

def get_monthly_user_games(username: str, year: int, month: int) -> list[JsonDict] | None:
    year_str = f"{year:04d}"
    month_str = f"{month:02d}"
    url = f"https://api.chess.com/pub/player/{username}/games/{year_str}/{month_str}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["games"]
    else:
        raise ChessComApiError(f"Could not get monthly history, API response code: {response.status_code}")
