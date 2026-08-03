from models.game import Game, GameOpening, GamePlayer
from models.enums import TimeClass
from datetime import datetime, timezone

EMPTY_RAW_GAME = {}
EXAMPLE_RAW_GAME_1 = {
      "url": "https://www.chess.com/game/live/76170873775",
      "pgn": "[Event \"Live Chess\"]\n[Site \"Chess.com\"]\n[Date \"2023.04.25\"]\n[Round \"-\"]\n[White \"Atefplays\"]\n[Black \"mrtinej\"]\n[Result \"1-0\"]\n[CurrentPosition \"Q7/1R6/k7/8/8/7K/8/8 b - -\"]\n[Timezone \"UTC\"]\n[ECO \"A00\"]\n[ECOUrl \"https://www.chess.com/openings/Van-Geet-Opening-Reversed-Nimzowitsch-Napoleon-Attack-3...exd4-4.Nxd4\"]\n[UTCDate \"2023.04.25\"]\n[UTCTime \"14:11:50\"]\n[WhiteElo \"893\"]\n[BlackElo \"874\"]\n[TimeControl \"600\"]\n[Termination \"Atefplays won by checkmate\"]\n[StartTime \"14:11:50\"]\n[EndDate \"2023.04.25\"]\n[EndTime \"14:21:22\"]\n[Link \"https://www.chess.com/game/live/76170873775\"]\n\n1. d4 {[%clk 0:10:00]} 1... e5 {[%clk 0:09:59.9]} 2. Nf3 {[%clk 0:09:58.6]} 2... Nc6 {[%clk 0:09:57]} 3. Nc3 {[%clk 0:09:51.4]} 3... exd4 {[%clk 0:09:54.5]} 4. Nxd4 {[%clk 0:09:49.3]} 4... Bb4 {[%clk 0:09:50.6]} 5. Nxc6 {[%clk 0:09:43.7]} 5... Bxc3+ {[%clk 0:09:48.8]} 6. bxc3 {[%clk 0:09:40.3]} 6... bxc6 {[%clk 0:09:48.7]} 7. e4 {[%clk 0:09:27]} 7... d5 {[%clk 0:09:46.2]} 8. Bd3 {[%clk 0:09:09.5]} 8... dxe4 {[%clk 0:09:41.9]} 9. Bxe4 {[%clk 0:09:07.2]} 9... Qxd1+ {[%clk 0:09:39.4]} 10. Kxd1 {[%clk 0:09:06.6]} 10... Nf6 {[%clk 0:09:36.1]} 11. Bxc6+ {[%clk 0:09:04.3]} 11... Kd8 {[%clk 0:09:33.4]} 12. Bxa8 {[%clk 0:09:03.5]} 12... Ng4 {[%clk 0:09:31.7]} 13. Bg5+ {[%clk 0:08:56.7]} 13... f6 {[%clk 0:09:29.8]} 14. Be3 {[%clk 0:08:51.9]} 14... f5 {[%clk 0:09:25.7]} 15. h3 {[%clk 0:08:49.9]} 15... Nxe3+ {[%clk 0:09:21.1]} 16. fxe3 {[%clk 0:08:46.6]} 16... Re8 {[%clk 0:09:19.2]} 17. Re1 {[%clk 0:08:44.3]} 17... g5 {[%clk 0:09:10.7]} 18. Ke2 {[%clk 0:08:40.8]} 18... f4 {[%clk 0:09:04.3]} 19. Bc6 {[%clk 0:08:39]} 19... Bd7 {[%clk 0:09:01.7]} 20. Bxd7 {[%clk 0:08:34.7]} 20... Kxd7 {[%clk 0:09:00.4]} 21. Rad1+ {[%clk 0:08:33.9]} 21... Kc8 {[%clk 0:08:58.4]} 22. Kf3 {[%clk 0:08:27.9]} 22... h5 {[%clk 0:08:52.4]} 23. exf4 {[%clk 0:08:26.8]} 23... gxf4 {[%clk 0:08:50.6]} 24. Kxf4 {[%clk 0:08:24.9]} 24... Rf8+ {[%clk 0:08:47.9]} 25. Kg3 {[%clk 0:08:21.5]} 25... Rg8+ {[%clk 0:08:45.2]} 26. Kh2 {[%clk 0:08:16.2]} 26... h4 {[%clk 0:08:41.9]} 27. Rg1 {[%clk 0:08:07.8]} 27... Re8 {[%clk 0:08:38.3]} 28. Rd2 {[%clk 0:08:03.8]} 28... c5 {[%clk 0:08:34.9]} 29. g3 {[%clk 0:08:02.3]} 29... Rh8 {[%clk 0:08:31.6]} 30. gxh4 {[%clk 0:08:00.6]} 30... Rxh4 {[%clk 0:08:29.1]} 31. Rg8+ {[%clk 0:07:55.9]} 31... Kb7 {[%clk 0:08:25.4]} 32. Rg6 {[%clk 0:07:54.8]} 32... a5 {[%clk 0:08:12]} 33. Rd5 {[%clk 0:07:46]} 33... Rc4 {[%clk 0:08:07.6]} 34. Rg4 {[%clk 0:07:33]} 34... Rxc3 {[%clk 0:08:05.2]} 35. Rd2 {[%clk 0:07:25.3]} 35... Kb6 {[%clk 0:08:00.8]} 36. h4 {[%clk 0:07:24.7]} 36... Re3 {[%clk 0:07:35.4]} 37. h5 {[%clk 0:07:21.4]} 37... Re7 {[%clk 0:07:33.2]} 38. Rg6+ {[%clk 0:07:15.5]} 38... Kb5 {[%clk 0:07:31]} 39. Rh6 {[%clk 0:07:10]} 39... c4 {[%clk 0:07:27.7]} 40. Rd5+ {[%clk 0:07:04]} 40... Kb4 {[%clk 0:07:25.8]} 41. Rh8 {[%clk 0:07:00.9]} 41... Kc3 {[%clk 0:07:20.9]} 42. Rxa5 {[%clk 0:06:57.8]} 42... Kxc2 {[%clk 0:07:18.8]} 43. h6 {[%clk 0:06:53]} 43... Kb2 {[%clk 0:07:08.7]} 44. h7 {[%clk 0:06:50.7]} 44... c3 {[%clk 0:07:06.5]} 45. Rh5 {[%clk 0:06:47]} 45... c2 {[%clk 0:07:04.6]} 46. Rc8 {[%clk 0:06:45.8]} 46... Re8 {[%clk 0:06:53]} 47. Rxc2+ {[%clk 0:06:40.4]} 47... Kxc2 {[%clk 0:06:51]} 48. a4 {[%clk 0:06:38.8]} 48... Re2+ {[%clk 0:06:42.6]} 49. Kh3 {[%clk 0:06:36.9]} 49... Re8 {[%clk 0:06:34.5]} 50. h8=Q {[%clk 0:06:34.6]} 50... Rxh8 {[%clk 0:06:29.2]} 51. Rxh8 {[%clk 0:06:34.5]} 51... Kb3 {[%clk 0:06:27.6]} 52. a5 {[%clk 0:06:33.8]} 52... Kc2 {[%clk 0:06:22]} 53. a6 {[%clk 0:06:33.7]} 53... Kd1 {[%clk 0:06:19.3]} 54. a7 {[%clk 0:06:33.6]} 54... Ke1 {[%clk 0:06:18]} 55. a8=Q {[%clk 0:06:33.5]} 55... Kf1 {[%clk 0:06:14.6]} 56. Rg8 {[%clk 0:06:32.1]} 56... Kf2 {[%clk 0:06:11.8]} 57. Qg2+ {[%clk 0:06:28.2]} 57... Ke3 {[%clk 0:06:10.4]} 58. Re8+ {[%clk 0:06:19.8]} 58... Kd3 {[%clk 0:06:06.7]} 59. Qb7 {[%clk 0:06:14.7]} 59... Kc4 {[%clk 0:06:05.2]} 60. Rc8+ {[%clk 0:06:07.6]} 60... Kd4 {[%clk 0:06:00.8]} 61. Qd7+ {[%clk 0:06:06.4]} 61... Ke5 {[%clk 0:05:59.4]} 62. Qe8+ {[%clk 0:05:59.5]} 62... Kd6 {[%clk 0:05:53.3]} 63. Rd8+ {[%clk 0:05:54]} 63... Kc7 {[%clk 0:05:50.1]} 64. Rd7+ {[%clk 0:05:42.8]} 64... Kc6 {[%clk 0:05:44.9]} 65. Qc8+ {[%clk 0:05:39.7]} 65... Kb6 {[%clk 0:05:42.1]} 66. Rb7+ {[%clk 0:05:37.5]} 66... Ka6 {[%clk 0:05:24.1]} 67. Qa8# {[%clk 0:05:37.4]} 1-0\n",
      "time_control": "600",
      "end_time": 1682432482,
      "rated": True,
      "tcn": "lB0Kgv5QbsKBvB9zBQzsjsXQmCZJftJCtC7ded!TCQ87Q4TEcM1TMuTLpxEunu?8he2MdmLD4Q6ZQZ7ZadZ6mv3NuDMDvD89Dw9!wpNFeg!8dlYIow8?wF?Fg!6X!UWGlJFAUEAsJlXPxFsuFNu0EUPHUVIAlJHzV?zsJGskNVkjV3AsGNsk?6086kjkiy8mpxm83~8?N?kryGrkGOkdOWdeW~ef?!fn4onu!8utoXtA86ABXZBKZ8KR67RY7ZYQ86QPZXPO64",
      "uuid": "1a7458d6-e373-11ed-912e-6cfe544c0428",
      "initial_setup": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
      "fen": "Q7/1R6/k7/8/8/7K/8/8 b - -",
      "time_class": "rapid",
      "rules": "chess",
      "white": {
        "rating": 893,
        "result": "win",
        "@id": "https://api.chess.com/pub/player/atefplays",
        "username": "Atefplays",
        "uuid": "38b1b876-5e73-11eb-848e-8bbe0e4c4660"
      },
      "black": {
        "rating": 874,
        "result": "checkmated",
        "@id": "https://api.chess.com/pub/player/mrtinej",
        "username": "mrtinej",
        "uuid": "94e0f1f4-f2c7-11ec-9fa5-01bc1e02a96b"
      },
      "eco": "https://www.chess.com/openings/Van-Geet-Opening-Reversed-Nimzowitsch-Napoleon-Attack-3...exd4-4.Nxd4"
}
EXAMPLE_RAW_GAME_2 = {
      "url": "https://www.chess.com/game/live/105808883125",
      "pgn": "[Event \"Live Chess\"]\n[Site \"Chess.com\"]\n[Date \"2024.04.02\"]\n[Round \"-\"]\n[White \"chess_blitz00\"]\n[Black \"Hikaru\"]\n[Result \"0-1\"]\n[Tournament \"https://www.chess.com/tournament/live/early-titled-tuesday-blitz-april-02-2024-4663138\"]\n[CurrentPosition \"8/8/1kp5/1p1p1K2/4r3/8/8/7R w - -\"]\n[Timezone \"UTC\"]\n[ECO \"C00\"]\n[ECOUrl \"https://www.chess.com/openings/French-Defense-St-George-Defense\"]\n[UTCDate \"2024.04.02\"]\n[UTCTime \"15:00:00\"]\n[WhiteElo \"2551\"]\n[BlackElo \"3264\"]\n[TimeControl \"180+1\"]\n[Termination \"Hikaru won on time\"]\n[StartTime \"15:00:00\"]\n[EndDate \"2024.04.02\"]\n[EndTime \"15:06:58\"]\n[Link \"https://www.chess.com/game/live/105808883125\"]\n\n1. e4 {[%clk 0:03:00.9]} 1... a6 {[%clk 0:02:58.4]} 2. d4 {[%clk 0:02:59.1]} 2... e6 {[%clk 0:02:58.1]} 3. Nc3 {[%clk 0:02:58.7]} 3... d5 {[%clk 0:02:57.1]} 4. exd5 {[%clk 0:02:56.7]} 4... exd5 {[%clk 0:02:57.1]} 5. Bd3 {[%clk 0:02:57.2]} 5... c6 {[%clk 0:02:57.1]} 6. Bf4 {[%clk 0:02:55]} 6... Bd6 {[%clk 0:02:49.7]} 7. Nge2 {[%clk 0:02:08.8]} 7... Bxf4 {[%clk 0:02:38.7]} 8. Nxf4 {[%clk 0:02:08.1]} 8... Qf6 {[%clk 0:02:39.6]} 9. Nfe2 {[%clk 0:01:56.4]} 9... Ne7 {[%clk 0:02:33.8]} 10. Qd2 {[%clk 0:01:54.1]} 10... Bf5 {[%clk 0:02:32.1]} 11. Bxf5 {[%clk 0:01:38.9]} 11... Nxf5 {[%clk 0:02:33]} 12. Qf4 {[%clk 0:01:28]} 12... Nd7 {[%clk 0:02:24.8]} 13. O-O-O {[%clk 0:01:10.4]} 13... O-O-O {[%clk 0:02:21.2]} 14. Ng3 {[%clk 0:01:01.6]} 14... Nh4 {[%clk 0:02:20.3]} 15. Qxf6 {[%clk 0:00:55.4]} 15... Nxf6 {[%clk 0:02:21.2]} 16. Rhg1 {[%clk 0:00:51.2]} 16... Rde8 {[%clk 0:02:15.4]} 17. f3 {[%clk 0:00:38.7]} 17... Re6 {[%clk 0:02:08.9]} 18. Rd2 {[%clk 0:00:34.4]} 18... Rhe8 {[%clk 0:02:08.4]} 19. Nge2 {[%clk 0:00:26.1]} 19... g5 {[%clk 0:02:07.9]} 20. Kd1 {[%clk 0:00:23]} 20... h5 {[%clk 0:02:03.5]} 21. Na4 {[%clk 0:00:19.3]} 21... Kc7 {[%clk 0:02:02.6]} 22. Nc5 {[%clk 0:00:19.2]} 22... R6e7 {[%clk 0:02:02.8]} 23. Nd3 {[%clk 0:00:19.3]} 23... Ng8 {[%clk 0:02:01.1]} 24. a4 {[%clk 0:00:17.4]} 24... Nf5 {[%clk 0:02:00]} 25. a5 {[%clk 0:00:14.9]} 25... Ne3+ {[%clk 0:02:00.1]} 26. Kc1 {[%clk 0:00:14.7]} 26... Nc4 {[%clk 0:02:01]} 27. Nc3 {[%clk 0:00:13.2]} 27... Nxa5 {[%clk 0:01:58.3]} 28. b3 {[%clk 0:00:12]} 28... b6 {[%clk 0:01:58.4]} 29. Ne5 {[%clk 0:00:10.4]} 29... Nb7 {[%clk 0:01:57.1]} 30. Kd1 {[%clk 0:00:06.3]} 30... Nd6 {[%clk 0:01:56.3]} 31. Re2 {[%clk 0:00:06.2]} 31... Nh6 {[%clk 0:01:48.7]} 32. Rge1 {[%clk 0:00:05.6]} 32... Nhf5 {[%clk 0:01:46.1]} 33. Rd2 {[%clk 0:00:04.5]} 33... f6 {[%clk 0:01:45.5]} 34. Nd3 {[%clk 0:00:04.9]} 34... Nxd4 {[%clk 0:01:39.5]} 35. Rxe7+ {[%clk 0:00:04.9]} 35... Rxe7 {[%clk 0:01:40.4]} 36. Nb4 {[%clk 0:00:05.4]} 36... N6f5 {[%clk 0:01:40.6]} 37. Nxa6+ {[%clk 0:00:04.9]} 37... Kb7 {[%clk 0:01:40.6]} 38. Nb4 {[%clk 0:00:05.3]} 38... Ne6 {[%clk 0:01:34.9]} 39. Ne2 {[%clk 0:00:04.4]} 39... Ne3+ {[%clk 0:01:34.7]} 40. Ke1 {[%clk 0:00:03.5]} 40... Nxg2+ {[%clk 0:01:35.6]} 41. Kf2 {[%clk 0:00:04]} 41... Ngf4 {[%clk 0:01:36.5]} 42. Nxf4 {[%clk 0:00:04]} 42... Nxf4 {[%clk 0:01:36.5]} 43. Nd3 {[%clk 0:00:02.6]} 43... Nxd3+ {[%clk 0:01:36.3]} 44. Rxd3 {[%clk 0:00:03.5]} 44... b5 {[%clk 0:01:35.8]} 45. b4 {[%clk 0:00:02.5]} 45... Kb6 {[%clk 0:01:36]} 46. c3 {[%clk 0:00:02.8]} 46... h4 {[%clk 0:01:33.1]} 47. h3 {[%clk 0:00:02.3]} 47... Ra7 {[%clk 0:01:32.5]} 48. f4 {[%clk 0:00:02.5]} 48... Ra2+ {[%clk 0:01:30.6]} 49. Kf3 {[%clk 0:00:02.8]} 49... Rh2 {[%clk 0:01:30.5]} 50. Kg4 {[%clk 0:00:03.3]} 50... Rg2+ {[%clk 0:01:30.3]} 51. Kf5 {[%clk 0:00:03.2]} 51... Rg3 {[%clk 0:01:30.8]} 52. Rd1 {[%clk 0:00:03.1]} 52... Rxc3 {[%clk 0:01:27.8]} 53. fxg5 {[%clk 0:00:03.5]} 53... fxg5 {[%clk 0:01:28.7]} 54. Kxg5 {[%clk 0:00:02.9]} 54... Rxh3 {[%clk 0:01:28.2]} 55. Rd4 {[%clk 0:00:03]} 55... Rc3 {[%clk 0:01:28]} 56. Rxh4 {[%clk 0:00:02.1]} 56... Rc4 {[%clk 0:01:28.4]} 57. Rh1 {[%clk 0:00:02.1]} 57... Rxb4 {[%clk 0:01:28.3]} 58. Kf5 {[%clk 0:00:03]} 58... Re4 {[%clk 0:01:28.3]} 0-1\n",
      "time_control": "180+1",
      "end_time": 1712070418,
      "rated": True,
      "accuracies": {
        "white": 83.26,
        "black": 89.57
      },
      "tcn": "mCWOlB0SbsZJCJSJftYQcD9RgmRDmD7TDm!0dl6LtL0LlD5Zec86mwLFDTZThg78nv8Sdl?8wm2Mcd3Nsy6YyIS0ItT!iyFLyGLudcuAmsAGjrXPtKGXcdXRlm!VgeVLml1TKtLBe080tzRLzOYXOzBSsmLudeuoenoDmDSDztDtltPHrzXPksNFpx0WvDWinvipvEpoELowtdwsDMTMLMsxdBxsBFsAFhAzMLzC",
      "uuid": "ad66a369-f101-11ee-b95b-6cfe544c0428",
      "initial_setup": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
      "fen": "8/8/1kp5/1p1p1K2/4r3/8/8/7R w - -",
      "time_class": "blitz",
      "rules": "chess",
      "white": {
        "rating": 2551,
        "result": "timeout",
        "@id": "https://api.chess.com/pub/player/chess_blitz00",
        "username": "chess_blitz00",
        "uuid": "168de2ea-65ac-11ee-b57e-c18318a1bc52"
      },
      "black": {
        "rating": 3264,
        "result": "win",
        "@id": "https://api.chess.com/pub/player/hikaru",
        "username": "Hikaru",
        "uuid": "6f4deb88-7718-11e3-8016-000000000000"
      },
      "eco": "https://www.chess.com/openings/French-Defense-St-George-Defense",
      "tournament": "https://api.chess.com/pub/tournament/early-titled-tuesday-blitz-april-02-2024-4663138"
}
EXAMPLE_OPENING_3 = {"eco": "https://www.chess.com/openings/A00-Example-Opening-1.e4-e5"}

EXPECTED_OPENING_1 = GameOpening(eco=None,
            opening_name="Van Geet Opening Reversed Nimzowitsch Napoleon Attack", 
            extended_moves = "3...exd4-4.Nxd4")
EXPECTED_OPENING_2 = GameOpening(eco=None,
            opening_name="French Defense St George Defense", 
            extended_moves = None)
EXPECTED_OPENING_3 = GameOpening(eco="A00",
            opening_name="Example Opening",
            extended_moves="1.e4-e5")

EXPECTED_GAME_1 = Game(
        white = GamePlayer(
                username = "atefplays",
                rating = 893,
                result = "win",
                accuracy = None
        ),
        black = GamePlayer(
                username = "mrtinej",
                rating = 874,
                result = "checkmated",
                accuracy = None
        ),
        played_at = datetime.fromtimestamp(1682432482, timezone.utc),
        time_class = TimeClass.RAPID,
        basetime = 600,
        increment = 0,
        opening = EXPECTED_OPENING_1,
        url = EXAMPLE_RAW_GAME_1["url"],
        raw_pgn = EXAMPLE_RAW_GAME_1["pgn"],
        rules = "chess",
        rated = True
)
EXPECTED_GAME_2 = Game(
        white = GamePlayer(
                username = "chess_blitz00",
                rating = 2551,
                result = "timeout",
                accuracy = 83.26
        ),
        black = GamePlayer(
                username = "hikaru",
                rating = 3264,
                result = "win",
                accuracy = 89.57
        ),
        played_at = datetime.fromtimestamp(1712070418, timezone.utc),
        time_class = TimeClass.BLITZ,
        basetime = 180,
        increment = 1,
        opening = EXPECTED_OPENING_2,
        url = EXAMPLE_RAW_GAME_2["url"],
        raw_pgn = EXAMPLE_RAW_GAME_2["pgn"],
        rules = "chess",
        rated = True
)

