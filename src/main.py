from db.database import SessionFactory
from db.repositories import GameRepository, ScrapeTargetRepository
from db.sync import SyncService


def main() -> None:
    game_repository = GameRepository(SessionFactory)
    scrape_target_repository = ScrapeTargetRepository(SessionFactory)

    sync_service = SyncService(
        session_factory=SessionFactory,
        game_repository=game_repository,
        scrape_target_repository=scrape_target_repository,
    )

    games = sync_service.sync_monthly_games(
        username="hikaru",
        year=2024,
        month=4,
    )
    if games:
        print(f"Loaded {len(games)} games")
    else:
        print("No games loaded")


if __name__ == "__main__":
    main()
