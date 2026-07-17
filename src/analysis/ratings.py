from data.chesscom_parser import build_monthly_gamelist
def get_peak_monthly_rating(username: str, year: str, month: str) -> int | None:
    gamelist = build_monthly_gamelist(username, year, month)
    if gamelist is None:
        return None
    ratings = []
    for game in gamelist:
        color = game.get_user_color(username)
        if color is None:
            continue
        ratings.append(getattr(game, color).rating)
    return max(ratings)