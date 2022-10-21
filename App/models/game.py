from App.database import db

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key=True)
    rawgId = db.Column(db.Integer, nullable=False)
    title =  db.Column(db.String(120), nullable=False)
    rating =  db.Column(db.String(20), nullable=False)
    platform =  db.Column(db.String(30), nullable=False)
    boxart =  db.Column(db.String(300), nullable=False)
    genre =  db.Column(db.String(20), nullable=False)
    listings = db.relationship('Listing', backref=db.backref('game', lazy='joined'))

    def __repr__(self):
        return f'<Game {self.gameId} - {self.title}>' 

    def toJSON(self):
        return {
            'gameId': self.gameId,
            'rawgId': self.rawgId,
            'title': self.title,
            'rating':self.rating,
            'platform': self.platform,
            'boxart': self.boxart,
            'genre': self.genre
        }

