from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from dotenv import dotenv_values
from pathlib import Path
from db.init_db import initialize_database
from db.base import Base
from db import models
from db.repositories import GameRepository, ScrapeTargetRepository
from db.sync import SyncService
import pytest
from data.chesscom_parser import build_gamelist_from_chesscom
from fixtures.raw_gamelist_data import (
    EXTENDED_RAW_GAMELIST, 
    EXTENDED_RAW_GAMELIST_2, 
    EXTENDED_RAW_GAMELIST_3,
    EXTENDED_RAW_GAMELIST_4,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
config = dotenv_values(PROJECT_ROOT / ".env")

TEST_DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=config['CHESSLAB_TEST_DB_USER'],
    password=config['CHESSLAB_TEST_DB_PASSWORD'],
    host=config['CHESSLAB_TEST_DB_HOST'],
    port=int(config.get('CHESSLAB_TEST_DB_PORT') or '3306'),
    database=config['CHESSLAB_TEST_DB_NAME']
)

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)
    initialize_database(engine)

    yield engine

    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session_factory(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    SessionFactory = sessionmaker(
        bind=connection,
        expire_on_commit=False
    )

    yield SessionFactory

    transaction.rollback()
    connection.close()

@pytest.fixture
def game_repository(db_session_factory):
    return GameRepository(db_session_factory)

@pytest.fixture
def scrape_target_repository(db_session_factory):
    return ScrapeTargetRepository(db_session_factory)

@pytest.fixture
def sync_service(db_session_factory, game_repository, scrape_target_repository):
    return SyncService(
        session_factory=db_session_factory,
        game_repository=game_repository,
        scrape_target_repository=scrape_target_repository,
    )

# Hikaru April 2024 partial
@pytest.fixture
def gamelist_1():
    gamelist_1 = build_gamelist_from_chesscom(EXTENDED_RAW_GAMELIST) 
    return [] if gamelist_1 is None else gamelist_1

# Atefplays April 2023 full
@pytest.fixture
def gamelist_2():
    gamelist_2 = build_gamelist_from_chesscom(EXTENDED_RAW_GAMELIST_2) 
    return [] if gamelist_2 is None else gamelist_2

# Hikaru 180+2 partial
@pytest.fixture
def gamelist_3():
    gamelist_3 = build_gamelist_from_chesscom(EXTENDED_RAW_GAMELIST_3)
    return [] if gamelist_3 is None else gamelist_3

# Hikaru 600 partial
@pytest.fixture
def gamelist_4():
    gamelist_4 = build_gamelist_from_chesscom(EXTENDED_RAW_GAMELIST_4)
    return [] if gamelist_4 is None else gamelist_4

@pytest.fixture
def mixed_user_gamelist(gamelist_1, gamelist_2):
    return gamelist_1 + gamelist_2

@pytest.fixture
def mixed_hikaru_gamelist(gamelist_1, gamelist_3):
    return gamelist_1 + gamelist_3

@pytest.fixture
def full_mixed_gamelist(gamelist_1, gamelist_3, gamelist_4):
    return gamelist_1 + gamelist_3 + gamelist_4


