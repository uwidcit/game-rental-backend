from App.database import db
from datetime import datetime

class Listing(db.Model):
    listingId = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer, db.ForeignKey('customer.id'))
    gameId = db.Column(db.Integer, db.ForeignKey('game.gameId'))
    condition = db.Column(db.String)
    price = db.Column(db.Float)
    status = db.Column(db.String)# available, rented, delisted
    created = db.Column(db.DateTime, default=datetime.utcnow)
    rentals = db.relationship('Rental', backref=db.backref('listing', lazy='joined'))

    def __init__(self, userId, gameId, condition="good", price=10.40):
        self.ownerId = userId
        self.gameId = gameId
        self.condition = condition
        self.price = price
        self.status = 'available'

    def __repr__(self):
        return f'<listing {self.listingId} for ${self.price}>'

    def toJSON_with_game(self):
        return{
            'listingId': self.listingId,
            'ownerId': self.ownerId,
            'condition': self.condition,
            'price': self.price,
            'status': self.status,
            'created': self.created.strftime("%Y/%m/%d, %H:%M:%S"),
            'game': self.game.toJSON(),
        }

    def toJSON(self):
        return{
            'title': self.game.title,
            'owner': self.ownerId,
            'condition': self.condition,
            'price': self.price,
            'created': self.created.strftime("%Y/%m/%d, %H:%M:%S"),
            'status': self.status
        }

