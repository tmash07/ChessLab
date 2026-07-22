from .base import Base
from datetime import datetime
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Boolean,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class GameModel(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True
    )
    played_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    basetime: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    increment: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    eco: Mapped[str | None] = mapped_column(
        String(5),
        nullable=True
    ) 
    rules: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    rated: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )
    raw_pgn: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    players: Mapped[list["GamePlayerModel"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_games_played_at", "played_at"),
        Index(
            "idx_games_time_control",
            "basetime",
            "increment"
        )
    )


class GamePlayerModel(Base):
    __tablename__ = "game_players"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )  
    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    color: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    result: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    game: Mapped[GameModel] = relationship(
        back_populates="players"
    )
    
    __table_args__ = (
        UniqueConstraint(
            "game_id",
            "color",
            name="uq_game_player_colors"
        ),
        Index(
            "idx_game_players_username",
            "username",
            "game_id"
        )
    )

class ScrapeTargetModel(Base):
    __tablename__ = "scrape_targets"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
    target_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )
    month: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )
    basetime: Mapped[int | None] = mapped_column(
        Integer, 
        nullable=True
    )
    increment: Mapped[int | None] = mapped_column(
        Integer, 
        nullable=True
    )
    last_successful_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    is_complete: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    __table_args__= (
        UniqueConstraint(
            "username",
            "year",
            "month",
            name="uq_monthly_scrape_target"
        ),
        UniqueConstraint(
            "username",
            "basetime",
            "increment",
            name="uq_time_control_scrape_target"
        ),
        CheckConstraint(
            """
            (
                target_type = 'monthly'
                AND year IS NOT NULL
                AND month IS NOT NULL
                AND basetime IS NULL
                AND increment IS NULL
            )
            OR
            (
                target_type = 'time_control'
                AND year IS NULL
                AND month IS NULL
                AND basetime IS NOT NULL
                AND increment IS NOT NULL
            )
            """
        )
    )