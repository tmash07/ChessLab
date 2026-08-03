import pytest
from analysis.filters import (
    filter_games,
    filter_by_color,
    filter_by_date_range,
    filter_by_opening_name,
    filter_by_time_class,
    filter_by_time_control,
    filter_by_user,
    group_by_opening_name_and_color
)
from analysis.summary_builder import build_performance_report, build_opening_report
from analysis.metrics import find_longest_win_streak, count_results
from models.enums import Color, TimeClass
from datetime import datetime, timezone
from models.summary import Record

# FILTER TESTS

def test_filter_games_on_empty_gamelist():
    gamelist = filter_games([], lambda game: True)
    assert len(gamelist) == 0

def test_filter_games(mixed_user_gamelist):
    gamelist = filter_games(mixed_user_gamelist, lambda game: True )
    assert len(gamelist) == 22

def test_filter_by_color(mixed_user_gamelist):
    gamelist = filter_by_color("hikaru", mixed_user_gamelist, Color.WHITE)
    assert len(gamelist) == 9

def test_filter_by_date_range(mixed_user_gamelist):
    gamelist = filter_by_date_range(mixed_user_gamelist, datetime(2023, 4, 28, tzinfo=timezone.utc), datetime(2024, 4, 3, tzinfo=timezone.utc))
    assert len(gamelist) == 20

def test_filter_by_opening_name(mixed_user_gamelist):
    gamelist = filter_by_opening_name(mixed_user_gamelist, "Trompowsky Attack")
    assert len(gamelist) == 3

def test_filter_by_time_class(mixed_user_gamelist):
    gamelist = filter_by_time_class(mixed_user_gamelist, TimeClass.RAPID)
    assert len(gamelist) == 4

def test_filter_by_time_control(mixed_user_gamelist):
    gamelist = filter_by_time_control(mixed_user_gamelist, 180, 1)
    assert len(gamelist) == 18

def test_filter_by_user(mixed_user_gamelist):
    gamelist = filter_by_user("hikaru", mixed_user_gamelist)
    assert len(gamelist) == 18

def test_group_by_opening_name_and_color(mixed_user_gamelist):
    groups = group_by_opening_name_and_color("hikaru", mixed_user_gamelist)
    assert len(groups[("French Defense St George Defense", Color.BLACK)]) == 3
    assert len(groups[("Clemenz Opening", Color.WHITE)]) == 1

# SUMMARY/METRIC TESTS

def test_build_performance_report(mixed_user_gamelist):
    report = build_performance_report("hikaru", mixed_user_gamelist)
    assert report.record == Record(wins=14, draws=3, losses=1)

    assert report.player_rating.count == 18
    assert report.player_rating.minimum == 3256
    assert report.player_rating.maximum == 3273

    assert report.rating_difference.count == 18
    assert report.rating_difference.total == 6999
    assert report.rating_difference.average == pytest.approx(6999/18)

    assert report.player_accuracy.missing == 0
    assert report.player_accuracy.maximum == 93.12

def test_build_opening_report(mixed_user_gamelist):
    report = build_opening_report("hikaru", mixed_user_gamelist, Color.WHITE, "Trompowsky Attack")

    assert report.record == Record(wins=3, draws=0, losses=0)

    assert report.opponent_rating.count == 3
    assert report.opponent_rating.minimum == 2885

    assert report.rating_difference.total == 739
    assert report.rating_difference.average == pytest.approx(739/3)

    assert report.opponent_accuracy.missing == 0
    assert report.opponent_accuracy.maximum == 86.57

def test_find_longest_win_streak(mixed_user_gamelist):
    longest = find_longest_win_streak("hikaru", mixed_user_gamelist)
    assert longest == 7

def test_count_results(mixed_user_gamelist):
    results = count_results("hikaru", mixed_user_gamelist)
    assert results["win"] == 14
    assert results["insufficient"] == 2









