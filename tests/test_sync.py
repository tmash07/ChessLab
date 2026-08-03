def test_sync_monthly_games(sync_service, gamelist_2, monkeypatch):
    def fake_build_monthly_gamelist(username, year, month):
        return gamelist_2
    monkeypatch.setattr(
        "db.sync.build_monthly_gamelist",
        fake_build_monthly_gamelist
    )

    result = sync_service.sync_monthly_games("atefplays", 2023, 4)
    assert result == gamelist_2

def test_sync_monthly_games_on_empty_gamelist(sync_service, gamelist_2, monkeypatch):
    def fake_build_monthly_gamelist(username, year, month):
        return []
    monkeypatch.setattr(
        "db.sync.build_monthly_gamelist",
        fake_build_monthly_gamelist
    )

    result = sync_service.sync_monthly_games("atefplays", 2023, 4)
    assert result == []

def test_sync_time_control_games(sync_service, gamelist_3, monkeypatch):
    def fake_build_time_control_gamelist(username, basetime, increment):
        return gamelist_3
    monkeypatch.setattr(
        "db.sync.build_time_control_gamelist",
        fake_build_time_control_gamelist
    )

    result = sync_service.sync_time_control_games("hikaru", 180, 2)
    assert result == gamelist_3

def test_sync_all_games_syncs_each_archive(sync_service, monkeypatch):
    calls = []
    monkeypatch.setattr(
        "db.sync.get_player_archives",
        lambda username: [
            "https://api.chess.com/pub/player/fabianocaruana/games/2013/03",
            "https://api.chess.com/pub/player/fabianocaruana/games/2013/04",
            "https://api.chess.com/pub/player/fabianocaruana/games/2013/05",
        ]
    )

    def fake_sync_monthly_games(username, year, month):
        calls.append((username, year, month))
        return [(year, month)]
    monkeypatch.setattr(
        sync_service,
        "sync_monthly_games",
        fake_sync_monthly_games
    )

    result = sync_service.sync_all_games("fabianocaruana")

    assert calls == [
        ("fabianocaruana", 2013, 3),
        ("fabianocaruana", 2013, 4),
        ("fabianocaruana", 2013, 5),
    ]

    assert result == [(2013, 3), (2013, 4), (2013, 5)]

def test_sync_all_games_syncs_on_empty_archives(sync_service, monkeypatch):
    calls = []
    monkeypatch.setattr(
        "db.sync.get_player_archives",
        lambda username: []
    )

    def fake_sync_monthly_games(username, year, month):
        calls.append((username, year, month))
        return [(year, month)]
    monkeypatch.setattr(
        sync_service,
        "sync_monthly_games",
        fake_sync_monthly_games
    )

    result = sync_service.sync_all_games("fabianocaruana")

    assert calls == []
    assert result == []









