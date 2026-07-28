from sqlalchemy.orm import sessionmaker
from .repositories import GameRepository, ScrapeTargetRepository
from models.scrape_target import ScrapeTarget
from models.game import Game
from data.chesscom_parser import build_monthly_gamelist, build_time_control_gamelist
from integrations.chesscom import get_player_archives
from datetime import datetime
from models.enums import ScrapeTargetType

class SyncService:
    def __init__(self, session_factory: sessionmaker, 
                 game_repository: GameRepository, 
                 scrape_target_repository: ScrapeTargetRepository) -> None:
        self._session_factory = session_factory
        self._game_repository = game_repository
        self._scrape_target_repository = scrape_target_repository
    
    def sync_monthly_games(self, username: str, year: int, month: int) -> list[Game]:
        username = self._normalize_and_validate_username(username)
        self._validate_monthly_args(year, month)

        target = self._scrape_target_repository.get_monthly_scrape_target(username, year, month)
        if target is None or not target.is_complete:
            games = build_monthly_gamelist(username, year, month)
            with self._session_factory.begin() as session:
                if games is None:
                    return []
                scrape_target = ScrapeTarget(
                    username=username,
                    target_type=ScrapeTargetType.MONTHLY,
                    year=year,
                    month=month,
                    basetime=None,
                    increment=None,
                    last_successful_at=datetime.now(),
                    is_complete=self._is_monthly_complete(year, month)
                )
                self._game_repository.save_games(session, games)
                self._scrape_target_repository.save_scrape_target(session, scrape_target)
            
        return self._game_repository.get_monthly_games(username, year, month)
    
    def sync_time_control_games(self, username: str, basetime: int, increment: int) -> list[Game]:
        username = self._normalize_and_validate_username(username)
        self._validate_time_control_args(basetime, increment)

        target = self._scrape_target_repository.get_basetime_scrape_target(username, basetime, increment)
        if target is None or not target.is_complete:
            games = build_time_control_gamelist(username, basetime, increment)
            with self._session_factory.begin() as session:
                if games is None:
                    return []
                scrape_target = ScrapeTarget(
                    username=username,
                    target_type=ScrapeTargetType.TIME_CONTROL,
                    year=None,
                    month=None,
                    basetime=basetime,
                    increment=increment,
                    last_successful_at=datetime.now(),
                    is_complete=False
                )
                self._game_repository.save_games(session, games)
                self._scrape_target_repository.save_scrape_target(session, scrape_target)
            
        return self._game_repository.get_time_control_games(username, basetime, increment)
    
    def sync_all_games(self, username: str) -> list[Game] | None:
        username = self._normalize_and_validate_username(username)

        archives = get_player_archives(username)
        if archives is None: 
            return None

        games = []
        for archive in archives:
            year_str, month_str = archive.rstrip("/").split("/")[-2:]
            year = int(year_str)
            month = int(month_str)
            monthly_games = self.sync_monthly_games(username, year, month)
            if monthly_games is not None: 
                games.extend(monthly_games)
        return games
    
    def _is_monthly_complete(self, year: int, month: int) -> bool:
        now = datetime.now()
        return (year, month) < (now.year, now.month)
    
    def _normalize_and_validate_username(self, username: str) -> str:
        username = username.strip().lower()
        if len(username) < 3 or len(username) > 20:
            raise ValueError("Username must be 3-20 characters in length")
        if any(c.isspace() for c in username):
            raise ValueError("Username contains whitespace")
        return username
    
    def _validate_monthly_args(self, year: int, month: int) -> None:
        now = datetime.now()
        if  not (2007 <= year <= now.year):
            raise ValueError(f"Year must be between 2007 and {now.year}")
        if not (1 <= month <= 12):
            raise ValueError(f"Month must be between 1 and 12")
        if (year, month) > (now.year, now.month):
            raise ValueError(f"Year/month cannot be in the future")
    
    def _validate_time_control_args(self, basetime: int, increment: int) -> None:
        if basetime <= 0:
            raise ValueError("Basetime must be a positive non-zero integer")
        if increment < 0:
            raise ValueError("Increment must be a non-negative integer")