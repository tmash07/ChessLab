from sqlalchemy.orm import sessionmaker
from .repositories import GameRepository, ScrapeTargetRepository

class SyncService:
    def __init__(self, session_factory: sessionmaker, 
                 game_repository: GameRepository, 
                 scrape_target_repository: ScrapeTargetRepository) -> None:
        self._session_factory = session_factory
        self._game_repository = game_repository
        self._scrape_target_repository = scrape_target_repository

