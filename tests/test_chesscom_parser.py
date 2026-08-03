from fixtures.raw_game_data import (
    EMPTY_RAW_GAME,
    EXAMPLE_RAW_GAME_1,
    EXAMPLE_RAW_GAME_2,
    EXAMPLE_OPENING_3,
    EXPECTED_OPENING_1,
    EXPECTED_OPENING_2,
    EXPECTED_OPENING_3,
    EXPECTED_GAME_1,
    EXPECTED_GAME_2
)
import pytest
from data.chesscom_parser import (
    get_basetime_increment,
    get_opening,
    build_game_from_chesscom,
    build_gamelist_from_chesscom,
    build_time_control_gamelist,
    build_monthly_gamelist
)

@pytest.mark.parametrize(
        "raw_game, expected_basetime_increment",
        [
            (EMPTY_RAW_GAME, None),
            (EXAMPLE_RAW_GAME_1, {"basetime": 600, "increment": 0}),
            (EXAMPLE_RAW_GAME_2, {"basetime": 180, "increment": 1}),
            ({"time_control": "invalid"}, None)
        ]
)
def test_get_basetime_increment(raw_game, expected_basetime_increment):
    time_control = get_basetime_increment(raw_game)
    assert time_control == expected_basetime_increment

@pytest.mark.parametrize(
        "raw_game, expected_opening",
        [
            (EMPTY_RAW_GAME, None),
            (EXAMPLE_RAW_GAME_1, EXPECTED_OPENING_1),
            (EXAMPLE_RAW_GAME_2, EXPECTED_OPENING_2),
            (EXAMPLE_OPENING_3, EXPECTED_OPENING_3)
        ]
)
def test_get_opening(raw_game, expected_opening):
    opening = get_opening(raw_game)
    assert opening == expected_opening

@pytest.mark.parametrize(
        "raw_game, expected_game",
        [
            (EMPTY_RAW_GAME, None),
            (EXAMPLE_RAW_GAME_1, EXPECTED_GAME_1),
            (EXAMPLE_RAW_GAME_2, EXPECTED_GAME_2)
        ]
)
def test_build_game_from_chesscom(raw_game, expected_game):
    game = build_game_from_chesscom(raw_game)
    assert game == expected_game

@pytest.mark.parametrize(
        "raw_gamelist, expected_gamelist",
        [
            ([], []),
            ([EXAMPLE_RAW_GAME_1], [EXPECTED_GAME_1]),
            ([EXAMPLE_RAW_GAME_1, EMPTY_RAW_GAME, EXAMPLE_RAW_GAME_2],
             [EXPECTED_GAME_1, EXPECTED_GAME_2])
        ]
)
def test_build_gamelist_from_chesscom(raw_gamelist, expected_gamelist):
    gamelist = build_gamelist_from_chesscom(raw_gamelist)
    assert gamelist == expected_gamelist

@pytest.mark.parametrize(
        "api_response, expected_gamelist",
        [
            ([], []),
            ([EXAMPLE_RAW_GAME_1], [EXPECTED_GAME_1]),
            ([EXAMPLE_RAW_GAME_1, EMPTY_RAW_GAME, EXAMPLE_RAW_GAME_2],
             [EXPECTED_GAME_1, EXPECTED_GAME_2])
        ]
)
def test_build_time_control_gamelist(monkeypatch, api_response, expected_gamelist):
    def fake_get_time_control_history(username, basetime, increment):
        return api_response
    
    monkeypatch.setattr(
        "data.chesscom_parser.get_time_control_history",
        fake_get_time_control_history
    )

    gamelist = build_time_control_gamelist("example", 600, 0)
    assert gamelist == expected_gamelist

@pytest.mark.parametrize(
        "api_response, expected_gamelist",
        [
            ([], []),
            ([EXAMPLE_RAW_GAME_1], [EXPECTED_GAME_1]),
            ([EXAMPLE_RAW_GAME_1, EMPTY_RAW_GAME, EXAMPLE_RAW_GAME_2],
             [EXPECTED_GAME_1, EXPECTED_GAME_2])
        ]
)
def test_build_monthly_gamelist(monkeypatch, api_response, expected_gamelist):
    def fake_get_monthly_user_games(username, year, month):
        return api_response
    
    monkeypatch.setattr(
        "data.chesscom_parser.get_monthly_user_games",
        fake_get_monthly_user_games
    )

    gamelist = build_monthly_gamelist("example", 2000, 1)
    assert gamelist == expected_gamelist


