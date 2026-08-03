from models.enums import Color, TimeClass
from fixtures.raw_game_data import EXPECTED_GAME_1
from fixtures.scrape_target_data import MONTHLY_SCRAPE_TARGET_1, TIME_CONTROL_SCRAPE_TARGET_1
from dataclasses import replace

# GAME REPOSITORY TESTS

def test_save_games_on_empty_gamelist(db_session_factory, game_repository):
    with db_session_factory() as session:
        game_repository.save_games(session, [])
        session.flush()
    
    games_from_db = game_repository.get_all_games("hikaru")
    assert len(games_from_db) == 0

def test_save_games_on_valid_gamelist(db_session_factory, game_repository, gamelist_1):
    with db_session_factory() as session:
        game_repository.save_games(session, gamelist_1)
        session.flush()
    
    games_from_db = game_repository.get_all_games("hikaru")
    assert len(games_from_db) == len(gamelist_1)

def test_get_monthly_games(db_session_factory, game_repository, mixed_hikaru_gamelist):
    with db_session_factory() as session:
        game_repository.save_games(session, mixed_hikaru_gamelist)
        session.flush()
    
    games_from_db = game_repository.get_monthly_games("hikaru", 2024, 4)
    assert len(games_from_db) == 18

def test_get_time_control_games(db_session_factory, game_repository, full_mixed_gamelist):
    with db_session_factory() as session:
        game_repository.save_games(session, full_mixed_gamelist)
        session.flush()
    
    games_from_db = game_repository.get_time_control_games("hikaru", 180, 2)
    assert len(games_from_db) == 29

def test_get_time_class_games(db_session_factory, game_repository, full_mixed_gamelist):
    with db_session_factory() as session:
        game_repository.save_games(session, full_mixed_gamelist)
        session.flush()
    
    games_from_db = game_repository.get_time_class_games("hikaru", TimeClass.RAPID)
    assert len(games_from_db) == 23

def test_get_color_games(db_session_factory, game_repository, full_mixed_gamelist):
    with db_session_factory() as session:
        game_repository.save_games(session, full_mixed_gamelist)
        session.flush()
    
    games_from_db = game_repository.get_color_games("hikaru", Color.WHITE)
    assert len(games_from_db) == 38

def test_orm_game_conversion(db_session_factory, game_repository):
    with db_session_factory() as session:
        game_repository.save_games(session, [EXPECTED_GAME_1])
        session.flush()
    
    games_from_db = game_repository.get_all_games("atefplays")
    game = games_from_db[0]

    assert game is not None
    assert game.url == EXPECTED_GAME_1.url
    assert game.played_at == EXPECTED_GAME_1.played_at
    assert game.time_class == EXPECTED_GAME_1.time_class
    assert game.white == EXPECTED_GAME_1.white
    assert game.raw_pgn == EXPECTED_GAME_1.raw_pgn

# SCRAPE TARGET REPOSITORY TESTS

def test_orm_scrape_target_conversion_and_saving(db_session_factory, scrape_target_repository):

    with db_session_factory() as session:
        scrape_target_repository.save_scrape_target(session, MONTHLY_SCRAPE_TARGET_1)
        scrape_target_repository.save_scrape_target(session, TIME_CONTROL_SCRAPE_TARGET_1)
        session.flush()
    
    monthly = scrape_target_repository.get_monthly_scrape_target("atefplays", 2023, 4)
    assert monthly is not None
    assert monthly.username == MONTHLY_SCRAPE_TARGET_1.username
    assert monthly.month == MONTHLY_SCRAPE_TARGET_1.month
    assert monthly.last_successful_at == MONTHLY_SCRAPE_TARGET_1.last_successful_at

    time_control = scrape_target_repository.get_basetime_scrape_target("hikaru", 180, 2)
    assert time_control is not None
    assert time_control.target_type == TIME_CONTROL_SCRAPE_TARGET_1.target_type
    assert time_control.basetime == TIME_CONTROL_SCRAPE_TARGET_1.basetime
    assert time_control.is_complete == TIME_CONTROL_SCRAPE_TARGET_1.is_complete

def test_scrape_target_updates(db_session_factory, scrape_target_repository):

    with db_session_factory() as session:
        scrape_target_repository.save_scrape_target(session, TIME_CONTROL_SCRAPE_TARGET_1)
        scrape_target_repository.save_scrape_target(session, 
                                                    replace(TIME_CONTROL_SCRAPE_TARGET_1, 
                                                            is_complete = True))
        session.flush()
    
    time_control = scrape_target_repository.get_basetime_scrape_target("hikaru", 180, 2)
    assert time_control is not None
    assert time_control.is_complete == True
    assert time_control.last_successful_at > TIME_CONTROL_SCRAPE_TARGET_1.last_successful_at
    










