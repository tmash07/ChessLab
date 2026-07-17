from models.game import Game

def filter_games_by_color(username: str, games_list: list[Game], color: str) -> list[Game]:
    filtered_games = []
    for game in games_list:
        game_color = game.get_user_color(username)
        if game_color == color:
            filtered_games.append(game)
    return filtered_games
        
