from models.summary import PerformanceReport, ColorReport, TimeClassReport, OpeningReport, Report
from models.game import Game
from models.enums import Color, TimeClass
from .metrics import *
from .filters import *
from dataclasses import asdict

def build_performance_report(user: str, games: list[Game]) -> PerformanceReport:
    return PerformanceReport(
        record=get_record(user, games),
        player_rating=build_numeric_summary(get_ratings(user, games)),
        opponent_rating=build_numeric_summary(get_opponent_ratings(user, games)),
        rating_difference=build_numeric_summary(get_rating_differences(user, games)),
        player_accuracy=build_numeric_summary(get_accuracies(user, games)),
        opponent_accuracy=build_numeric_summary(get_opponent_accuracies(user, games)),
        total_games=len(filter_by_user(user, games))
    )

def build_color_report(user: str, games: list[Game], color: Color) -> ColorReport:
    filtered_games = filter_by_color(user, games, color)
    report = build_performance_report(user, filtered_games)
    return ColorReport(**report.report_fields(), color=color)

def build_time_class_report(user: str, games: list[Game], time_class: TimeClass) -> TimeClassReport:
    filtered_games = filter_by_time_class(games, time_class)
    report = build_performance_report(user, filtered_games)
    return TimeClassReport(**report.report_fields(), time_class=time_class)

def build_opening_report(user: str, games: list[Game], color: Color, opening: str) -> OpeningReport:
    filtered_games = filter_by_opening_name(games, opening)
    report = build_color_report(user, filtered_games, color)
    return OpeningReport(**report.report_fields(), opening_name=opening)