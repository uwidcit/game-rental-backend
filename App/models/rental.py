from App.database import db
from datetime import datetime

DEFAULT_RENTAL_PEROID = 14

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
    
    def calculate_fees(self):
        days_rented = (self.return_date - self.rental_date).days
        days_late = days_rented - DEFAULT_RENTAL_PEROID
        if days_late > 0:
            return self.listing.price + ( 0.10 * self.listing.price * days_late )
        return self.listing.price

    def return_rental(self):
         self.rental_date = datetime.utcnow
         fees = self.calculate_fees()
         rental.listing.status = 'available'
         db.session.add(self)
         db.session.add(self.listing)
         db.session.commit()
         return fees
         

    def toJSON(self):
        return{
            'rentalId': self.rentalId,
            'userId': self.userId,
            'listingId': self.listingId,
            'rental_date': self.rental_date.strftime("%Y/%m/%d, %H:%M:%S"),
            'return_date': self.return_date.strftime("%Y/%m/%d, %H:%M:%S") if self.return_date else None
        }