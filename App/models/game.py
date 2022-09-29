
from App.database import db

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(120), nullable=False)
    rating =  db.Column(db.String(20), nullable=False)
    platform =  db.Column(db.String(30), nullable=False)
    boxart =  db.Column(db.String(300), nullable=False)
    genre =  db.Column(db.String(20), nullable=False)
    

    def __repr__(self):
        return f'<Game {self.gameId} - {self.title}>' 

    def toJSON(self):
        return{
            'id': self.gameId,
            'title': self.title,
            'rating':self.rating,
            'platform': self.platform,
            'boxart': self.boxart,
            'genre': self.genre
        }