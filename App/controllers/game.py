from App.models import Game
from App.database import db
from App.config import load_config

import requests

config = load_config()


def create_game(title, rating='Teen', platform='ps5', boxart='https://placecage.com/500/500', genre='action'):
    newgame = Game(title=title, rating=rating, platform=platform, boxart=boxart, genre=genre)
    db.session.add(newgame)
    db.session.commit()
    return newgame

def get_all_games():
    return Game.query.all()

def fetch_api_games():
    url = f'https://api.rawg.io/api/games?key={config["RAWG_TOKEN"]}'
    print(url)
    response = requests.request("GET", url)
    return response.text

def populate_games():
    Game.query.delete()
    db.session.commit()

def get_all_games_json():
    games = Game.query.all()
    if not games:
        return []
    return [game.toJSON() for game in games]
