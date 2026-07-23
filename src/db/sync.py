from sqlalchemy.orm import sessionmaker
from .repositories import GameRepository, ScrapeTargetRepository
from models.scrape_target import ScrapeTarget
from data.chesscom_parser import build_monthly_gamelist, build_time_control_gamelist
from datetime import datetime

class SyncService:
    def __init__(self, session_factory: sessionmaker, 
                 game_repository: GameRepository, 
                 scrape_target_repository: ScrapeTargetRepository) -> None:
        self._session_factory = session_factory
        self._game_repository = game_repository
        self._scrape_target_repository = scrape_target_repository
    
    def sync_monthly_games(self, username: str, year: int, month: int):
        target = self._scrape_target_repository.get_monthly_scrape_target(username, year, month)

        if target is None or not target.is_complete:
            games = build_monthly_gamelist(username, year, month)
            with self._session_factory.begin() as session:
                if games is None:
                    return
                scrape_target = ScrapeTarget(
                    username=username,
                    target_type="monthly",
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
    
    def sync_time_control_games(self, username: str, basetime: int, increment: int):
        target = self._scrape_target_repository.get_basetime_scrape_target(username, basetime, increment)

        if target is None or not target.is_complete:
            games = build_time_control_gamelist(username, str(basetime), str(increment))
            with self._session_factory.begin() as session:
                if games is None:
                    return
                scrape_target = ScrapeTarget(
                    username=username,
                    target_type="time_control",
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
    
    def _is_monthly_complete(self, year: int, month: int) -> bool:
        now = datetime.now()
        return (year, month) < (now.year, now.month)