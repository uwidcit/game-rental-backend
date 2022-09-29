from App.database import db
from datetime import datetime

class Rental(db.Model):
    rentalId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    listingId = db.Column(db.Integer, db.ForeignKey('listing.listingId'))
    rental_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, default=None)

    def __init__(self, userId, listingId):
        self.userId = userId
        self.listingId = listingId
    
    def __repr__(self):
        return f'<rental {self.rentalId} >'
    
    def toJSON(self):
        return{
            'rentalId': self.rentalId,
            'userId': self.userId,
            'listingId': self.listingId,
            'rental_date': self.rental_date.strftime("%Y/%m/%d, %H:%M:%S"),
            'return_date': self.return_date.strftime("%Y/%m/%d, %H:%M:%S") if self.return_date else None
        }