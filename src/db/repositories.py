from sqlalchemy.orm import sessionmaker, Session
from models.game import Game
from models.scrape_target import ScrapeTarget
from db.models import GameModel, GamePlayerModel, ScrapeTargetModel
from sqlalchemy import select

class GameRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def add_games(self, session: Session, games: list[Game]) -> None:
        models = [self._game_to_orm(game) for game in games]
        session.add_all(models)
    
    def _game_to_orm(self, game: Game) -> GameModel:
        white_player = GamePlayerModel(
            username=game.white.username,
            color="white",
            rating=game.white.rating,
            result=game.white.result
        )
        black_player = GamePlayerModel(
            username=game.black.username,
            color="black",
            rating=game.black.rating,
            result=game.black.result
        )

        return GameModel(
            url=game.url,
            played_at=game.played_at,
            basetime=game.basetime,
            increment=game.increment,
            eco=game.eco,
            rules=game.rules,
            rated=game.rated,
            raw_pgn=game.raw_pgn,
            players=[white_player, black_player]
        )
    
class ScrapeTargetRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def add_scrape_target(self, session: Session, scrape_target: ScrapeTarget):
        model = self._scrape_target_to_orm(scrape_target)
        session.add(model) 

    def get_monthly_scrape_target(self, session: Session, username: str, year: int, month: int) -> ScrapeTarget | None:
        statement = select(ScrapeTargetModel).where(
            ScrapeTargetModel.username == username,
            ScrapeTargetModel.target_type == "monthly",
            ScrapeTargetModel.year == year,
            ScrapeTargetModel.month == month
        )
        model = session.scalar(statement)
        if model is None: return None

        return self._orm_to_scrape_target(model)
    
    def _scrape_target_to_orm(self, scrape_target: ScrapeTarget) -> ScrapeTargetModel:
        return ScrapeTargetModel(
            username=scrape_target.username,
            target_type=scrape_target.target_type,
            year=scrape_target.year,
            month=scrape_target.month,
            basetime=scrape_target.basetime,
            increment=scrape_target.increment,
            last_successful_at=scrape_target.last_successful_at,
            is_complete=scrape_target.is_complete
        )
    
    def _orm_to_scrape_target(self, model: ScrapeTargetModel) -> ScrapeTarget:
        return ScrapeTarget(
            username=model.username,
            target_type=model.target_type,
            year=model.year,
            month=model.month,
            basetime=model.basetime,
            increment=model.increment,
            last_successful_at=model.last_successful_at,
            is_complete=model.is_complete
        )