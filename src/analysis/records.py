win_codes = ["win"]
draw_codes = ["agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"]
loss_codes = ["checkmated", "timeout", "resigned", "lose", "abandoned", "kingofthehill", "threecheck", "bughousepartnerlose"]
    
def get_record(username, games_list):
    record = {"wins": 0, "draws": 0, "losses": 0}
    for game in games_list:
        color = "white" if game["white"]["username"] == username else "black"
        result = game[color]["result"]  
        if (result in win_codes):
            record["wins"] += 1
        elif (result in draw_codes):
            record["draws"] += 1
        elif (result in loss_codes):
            record["losses"] += 1
        else:
            print("Error: result code not recognized")
    return record

