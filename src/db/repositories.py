from sqlalchemy.orm import sessionmaker, Session, selectinload
from models.game import Game, GamePlayer, GameOpening
from models.scrape_target import ScrapeTarget
from db.models import GameModel, GamePlayerModel, GameOpeningModel, ScrapeTargetModel
from sqlalchemy import select, and_
from datetime import datetime
from models.enums import Color, ScrapeTargetType, TimeClass

class GameRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def add_games(self, session: Session, games: list[Game]) -> None:
        models = [self._game_to_orm(game) for game in games]
        session.add_all(models)

    def save_games(self, session: Session, games: list[Game]) -> None:
        if not games: return

        games_by_url = {game.url : game for game in games}
        statement = select(GameModel.url).where(GameModel.url.in_(games_by_url))
        existing_urls = set(session.scalars(statement).all())

        new_games = [game for url, game in games_by_url.items() if url not in existing_urls]
        self.add_games(session, new_games)


    def get_monthly_games(self, username: str, year: int, month: int) -> list[Game]:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        statement = (select(GameModel).where(
            GameModel.players.any(
                GamePlayerModel.username == username
            ),
            GameModel.played_at >= start_date,
            GameModel.played_at < end_date
        )
        .options(
            selectinload(GameModel.players),
            selectinload(GameModel.opening)
        )        
        .order_by(GameModel.played_at)
        )
        
        with self._session_factory() as session:
            models = session.scalars(statement).all()

        return [self._orm_to_game(model) for model in models]
    
    def get_time_control_games(self, username: str, basetime: int, increment: int) -> list[Game]:
        statement = (select(GameModel).where(
            GameModel.players.any(
                GamePlayerModel.username == username
            ),
            GameModel.basetime == basetime,
            GameModel.increment == increment
        )
        .options(
            selectinload(GameModel.players),
            selectinload(GameModel.opening)
        )
        .order_by(GameModel.played_at)
        )
        
        with self._session_factory() as session:
            models = session.scalars(statement).all()

        return [self._orm_to_game(model) for model in models]
    
    def get_time_class_games(self, username: str, time_class: TimeClass) -> list[Game]:
        statement = (select(GameModel).where(
            GameModel.players.any(
                GamePlayerModel.username == username
            ),
            GameModel.time_class == time_class.value
        )
        .options(
            selectinload(GameModel.players),
            selectinload(GameModel.opening)
        )
        .order_by(GameModel.played_at)
        )
        
        with self._session_factory() as session:
            models = session.scalars(statement).all()

        return [self._orm_to_game(model) for model in models]
    
    def get_color_games(self, username: str, color: Color) -> list[Game]:
        statement = (select(GameModel).where(
            GameModel.players.any(
                and_(
                    GamePlayerModel.color == color.value,
                    GamePlayerModel.username == username
                )
            )
        )
        .options(
            selectinload(GameModel.players),
            selectinload(GameModel.opening)
        )
        .order_by(GameModel.played_at)
        )

        with self._session_factory() as session:
            models = session.scalars(statement).all()
        
        return [self._orm_to_game(model) for model in models]
    
    def get_all_games(self, username: str) -> list[Game]:
        statement = (select(GameModel).where(
            GameModel.players.any(
                GamePlayerModel.username == username
            )
        )
        .options(
            selectinload(GameModel.players),
            selectinload(GameModel.opening)
        )        
        .order_by(GameModel.played_at)
        )

        with self._session_factory() as session:
            models = session.scalars(statement).all()
        
        return [self._orm_to_game(model) for model in models]
    
    def _game_to_orm(self, game: Game) -> GameModel:
        white_player = GamePlayerModel(
            username=game.white.username,
            color=Color.WHITE.value,
            rating=game.white.rating,
            result=game.white.result,
            accuracy=game.white.accuracy
        )
        black_player = GamePlayerModel(
            username=game.black.username,
            color=Color.BLACK.value,
            rating=game.black.rating,
            result=game.black.result,
            accuracy=game.black.accuracy
        )
        opening = GameOpeningModel(
            eco=game.opening.eco,
            opening_name=game.opening.opening_name,
            extended_moves=game.opening.extended_moves
        )
        return GameModel(
            url=game.url,
            played_at=game.played_at,
            basetime=game.basetime,
            increment=game.increment,
            time_class=game.time_class.value,
            opening=opening,
            rules=game.rules,
            rated=game.rated,
            raw_pgn=game.raw_pgn,
            players=[white_player, black_player]
        )
    
    def _orm_to_game(self, model: GameModel) -> Game:
        players_by_color = {player.color: player for player in model.players}
        if Color.WHITE.value not in players_by_color or Color.BLACK.value not in players_by_color:
            raise ValueError("White or black player is missing from game")
        white_model = players_by_color[Color.WHITE.value]
        black_model = players_by_color[Color.BLACK.value]
        white_player = GamePlayer(
            username=white_model.username,
            rating=white_model.rating,
            result=white_model.result,
            accuracy=white_model.accuracy
        )
        black_player = GamePlayer(
            username=black_model.username,
            rating=black_model.rating,
            result=black_model.result,
            accuracy=black_model.accuracy
        )
        opening = GameOpening(
            eco=model.opening.eco,
            opening_name=model.opening.opening_name,
            extended_moves=model.opening.extended_moves
        )
        return Game(
            white=white_player,
            black=black_player,
            played_at=model.played_at,
            time_class=TimeClass(model.time_class),
            basetime=model.basetime,
            increment=model.increment,
            opening=opening,
            url=model.url,
            raw_pgn=model.raw_pgn,
            rules=model.rules,
            rated=model.rated
        )
    
class ScrapeTargetRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def add_scrape_target(self, session: Session, scrape_target: ScrapeTarget) -> None:
        model = self._scrape_target_to_orm(scrape_target)
        session.add(model) 

    def save_scrape_target(self, session: Session, scrape_target: ScrapeTarget) -> None:
        if scrape_target.target_type == ScrapeTargetType.MONTHLY:
            statement = select(ScrapeTargetModel).where(
                ScrapeTargetModel.username == scrape_target.username,
                ScrapeTargetModel.target_type == ScrapeTargetType.MONTHLY.value,
                ScrapeTargetModel.year == scrape_target.year,
                ScrapeTargetModel.month == scrape_target.month,
        )
        elif scrape_target.target_type == ScrapeTargetType.TIME_CONTROL:
            statement = select(ScrapeTargetModel).where(
                ScrapeTargetModel.username == scrape_target.username,
                ScrapeTargetModel.target_type == ScrapeTargetType.TIME_CONTROL.value,
                ScrapeTargetModel.basetime == scrape_target.basetime,
                ScrapeTargetModel.increment == scrape_target.increment,
        )
        else:
            raise ValueError("Invalid target type")
            
        model = session.scalar(statement)

        if model is None:
            self.add_scrape_target(session, scrape_target)
            return
        model.last_successful_at = datetime.now()
        model.is_complete = scrape_target.is_complete


    def get_monthly_scrape_target(self, username: str, year: int, month: int) -> ScrapeTarget | None:
        statement = select(ScrapeTargetModel).where(
            ScrapeTargetModel.username == username,
            ScrapeTargetModel.target_type == ScrapeTargetType.MONTHLY.value,
            ScrapeTargetModel.year == year,
            ScrapeTargetModel.month == month
        )
        with self._session_factory() as session:
            model = session.scalar(statement)
        if model is None: return None

        return self._orm_to_scrape_target(model)
    
    def get_basetime_scrape_target(self, username: str, basetime: int, increment: int) -> ScrapeTarget | None:
        statement = select(ScrapeTargetModel).where(
            ScrapeTargetModel.username == username,
            ScrapeTargetModel.target_type == ScrapeTargetType.TIME_CONTROL.value,
            ScrapeTargetModel.basetime == basetime,
            ScrapeTargetModel.increment == increment
        )

        with self._session_factory() as session:
            model = session.scalar(statement)
        if model is None: return None

        return self._orm_to_scrape_target(model)
    
    def _scrape_target_to_orm(self, scrape_target: ScrapeTarget) -> ScrapeTargetModel:
        return ScrapeTargetModel(
            username=scrape_target.username,
            target_type=scrape_target.target_type.value,
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
            target_type=ScrapeTargetType(model.target_type),
            year=model.year,
            month=model.month,
            basetime=model.basetime,
            increment=model.increment,
            last_successful_at=model.last_successful_at,
            is_complete=model.is_complete
        )