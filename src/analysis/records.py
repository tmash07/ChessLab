from models.game import Game
from collections import Counter

win_codes = ["win"]
draw_codes = ["agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"]
loss_codes = ["checkmated", "timeout", "resigned", "lose", "abandoned", "kingofthehill", "threecheck", "bughousepartnerlose"]
    
def get_record(username: str, games_list: list[Game]) -> Counter[str]:
    record = Counter()
    for game in games_list:
        color = game.get_user_color(username)
        if color is None:
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

