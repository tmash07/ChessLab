from models.game import Game
from collections import Counter
from data.chesscom_parser import build_time_control_gamelist, build_monthly_gamelist


win_codes = ["win"]
draw_codes = ["agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"]
loss_codes = ["checkmated", "timeout", "resigned", "lose", "abandoned", "kingofthehill", "threecheck", "bughousepartnerlose"]
    
def get_record(username: str, games_list: list[Game]) -> Counter[str]:
    record = Counter()
    for game in games_list:
        color = game.get_user_color(username)
        if color is None:
            continue
        if game.rules != "chess":
            continue
        result = game.white.result if color == "white" else game.black.result 
        if (result in win_codes):
            record["wins"] += 1
        elif (result in draw_codes):
            record["draws"] += 1
        elif (result in loss_codes):
            record["losses"] += 1
        else:
            print("Error: result code not recognized")
    return record

def get_time_control_record(username: str, basetime: str, increment: str) -> Counter[str] | None:
    gamelist = build_time_control_gamelist(username, basetime, increment)
    if gamelist is None:
        return None
    return get_record(username, gamelist)

def get_monthly_record(username: str, year: str, month: str) -> Counter[str] | None:
    gamelist = build_monthly_gamelist(username, year, month)
    if gamelist is None:
        return None
    return get_record(username, gamelist)

