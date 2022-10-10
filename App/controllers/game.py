from App.models import Game
from App.database import db

def create_game(title, rating='Teen', platform='ps5', boxart='https://placecage.com/500/500', genre='action'):
    newgame = Game(title=title, rating=rating, platform=platform, boxart=boxart, genre=genre)
    db.session.add(newgame)
    db.session.commit()
    return newgame

def get_all_games():
    return Game.query.all()

def get_all_games_json():
    games = Game.query.all()
    if not games:
        return []
    return [game.toJSON() for game in games]
