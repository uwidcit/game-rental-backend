
from App.database import db

class Listing(db.Model):
    listingId = db.Column(db.Integer, primary_key=True)
    gameId = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    ownerId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    condition =  db.Column(db.String(120), nullable=False)
    availability =  db.Column(db.String(20), nullable=False)
    price =  db.Column(db.Double, nullable=False)
    

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