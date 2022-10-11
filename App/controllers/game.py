from App.models import Game
from App.database import db
from App.config import config
import requests
import json


def create_game(title, rawgId, rating='Teen', platform='ps5', boxart='https://placecage.com/500/500', genre='action'):
    newgame = Game(title=title, rawgId=rawgId, rating=rating, platform=platform, boxart=boxart, genre=genre)
    db.session.add(newgame)
    db.session.commit()
    return newgame

def get_game(rawgId):
    game = Game.query.filter_by(rawgId=rawgId).first()
    if game :
        return game
    else:
        game = fetch_api_game(rawgId)
        if game:
            rating = "N/S"
            if game['esrb_rating']:
                rating = game['esrb_rating']['name']
            game = create_game(title=game['name'], rawgId=game['id'], rating=rating, boxart=game['background_image'], genre=game['genres'][0]['slug'])
            return game
    return None

def get_all_games():
    return Game.query.all()

def fetch_api_game(rawgId):
    url = f'https://api.rawg.io/api/games/{rawgId}?key={config["RAWG_TOKEN"]}'
    response = requests.request("GET", url)
    return json.loads(response.text)

def fetch_api_games():
    url = f'https://api.rawg.io/api/games?key={config["RAWG_TOKEN"]}'
    response = requests.request("GET", url)
    json_response = json.loads(response.text)
    return json_response['results']

def populate_games():
    Game.query.delete()
    db.session.commit()

def get_all_games_json():
    games = Game.query.all()
    if not games:
        return []
    return [game.toJSON() for game in games]
