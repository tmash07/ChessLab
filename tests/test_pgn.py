from data.pgn import (
    get_headers_from_pgn,
    get_ratings, 
    get_users,
    get_user_color,
    get_opening,
    get_date_and_time
)
from models.enums import Color
from fixtures.pgn_data import (
    EMPTY_PGN, 
    MINIMAL_PGN, 
    EXAMPLE_PGN_1, 
    EXAMPLE_PGN_2, 
    EMPTY_HEADERS,
    EXAMPLE_HEADERS_1,
    EXAMPLE_HEADERS_2
)
from datetime import datetime
import pytest

@pytest.mark.parametrize(
        "pgn",
        [
            MINIMAL_PGN,
            EXAMPLE_PGN_1,
            EXAMPLE_PGN_2
        ]
)
def test_get_headers_from_pgn_returns_required_headers(pgn):
    headers = get_headers_from_pgn(pgn)

    assert headers is not None
    assert all(x in headers for x in ["Event", "Site", "Date", "Round", "White", "Black", "Result"])

def test_get_headers_from_pgn_returns_none_for_empty():
    headers = get_headers_from_pgn(EMPTY_PGN)
    assert headers is None

@pytest.mark.parametrize(
        "headers, expected_white, expected_black",
        [
            (EMPTY_HEADERS, None, None),
            (EXAMPLE_HEADERS_1, 893, 874),
            (EXAMPLE_HEADERS_2, 2551, 3264)
        ]
)
def test_get_ratings(headers, expected_white, expected_black):
    ratings = get_ratings(headers)
    assert ratings[Color.WHITE] == expected_white
    assert ratings[Color.BLACK] == expected_black

@pytest.mark.parametrize(
        "headers, expected_white, expected_black",
        [
            (EMPTY_HEADERS, None, None),
            (EXAMPLE_HEADERS_1, "Atefplays", "mrtinej"),
            (EXAMPLE_HEADERS_2, "chess_blitz00", "Hikaru")
        ]
)
def test_get_users(headers, expected_white, expected_black):
    users = get_users(headers)
    assert users[Color.WHITE] == expected_white
    assert users[Color.BLACK] == expected_black

def test_get_user_color_returns_none_for_unknown_user():
    color = get_user_color("ExampleUser", EXAMPLE_HEADERS_1)
    assert color is None

@pytest.mark.parametrize(
        "headers, white_user, black_user",
        [
            (EXAMPLE_HEADERS_1, "Atefplays", "mrtinej"),
            (EXAMPLE_HEADERS_2, "chess_blitz00", "Hikaru")
        ]
)
def test_get_user_color_correctly_finds_color(headers, white_user, black_user):
    white = get_user_color(white_user, headers)
    black = get_user_color(black_user, headers)
    assert white == Color.WHITE
    assert black == Color.BLACK

@pytest.mark.parametrize(
        "headers, expected_opening",
        [
            (EMPTY_HEADERS, None),
            (EXAMPLE_HEADERS_1, "A00"),
            (EXAMPLE_HEADERS_2, "C00")
        ]
)
def test_get_opening(headers, expected_opening):
    opening = get_opening(headers)
    assert opening == expected_opening

@pytest.mark.parametrize(
        "headers, expected_datetime",
        [
            (EMPTY_HEADERS, None),
            (EXAMPLE_HEADERS_1, datetime(2023, 4, 25, 14, 11, 50)),
            (EXAMPLE_HEADERS_2, datetime(2024, 4, 2, 15, 0, 0))
        ]
)
def test_get_date_and_time(headers, expected_datetime):
    date_and_time = get_date_and_time(headers)
    assert date_and_time == expected_datetime