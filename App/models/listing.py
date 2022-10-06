from App.database import db
from datetime import datetime

class Listing(db.Model):
    listingId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    gameId = db.Column(db.Integer, db.ForeignKey('game.gameId'))
    condition = db.Column(db.String)
    price = db.Column(db.Float)
    status = db.Column(db.String)# available, rented, delisted
    created = db.Column(db.DateTime, default=datetime.utcnow)
    rentals = db.relationship('Rental', backref=db.backref('listing', lazy='joined'))

    def __init__(self, userId, gameId, condition="good", price=10.40):
        self.userId = userId
        self.gameId = gameId
        self.condition = condition
        self.status = 'available'
        self.price = price

    def __repr__(self):
        return f'<listing {self.listingId} - {self.game.title} - listed by {self.user.username} for ${self.price}>'

    def toJSON_with_game(self):
        return{
            'title': self.game.title,
            'condition': self.condition,
            'price': self.price,
            'created': self.created.strftime("%Y/%m/%d, %H:%M:%S"),
            'status': self.status,
            'game': self.game.toJSON(),
        }

    def toJSON(self):
        return{
            'title': self.game.title,
            'condition': self.condition,
            'price': self.price,
            'created': self.created.strftime("%Y/%m/%d, %H:%M:%S"),
            'status': self.status
        }

