import json
import logging
from datetime import date

import pandas
import requests
from constants import CHESS_BASE_API_URI, USERNAME

logger = logging.getLogger(__name__)


def build_api_uri():
    return f"{CHESS_BASE_API_URI}/{USERNAME}/games/{date.today().year}/{date.today().month}"


def get_games(uri):
    game_request = requests.get(
        uri,
        headers={  # These are necessary as the default headers will get a 403 from chess.com
            "User-Agent": "FollowK Python Application. "
        },
    )
    if game_request.status_code != 200:
        logger.error(game_request.status_code)
        logger.error(game_request.request.body)
        logger.error(game_request.request.headers)
        logger.error(game_request.reason)
        logger.error(uri)
        raise ("Fetching game failed")
    return game_request.content


def process_game(game):
    color = "white" if game.white["username"] == "FollowK" else "black"
    result = game[color]["result"]

    return result, color


def get_win_status(game):
    return game[game.color]["result"]


if __name__ == "__main__":
    games_uri = build_api_uri()
    unformated_games = get_games(uri=games_uri)
    games_df = pandas.DataFrame(json.loads(unformated_games)["games"])
    games_df[["result", "color"]] = games_df.apply(process_game, axis=1)
    print(games_df[["color", "result"]])
