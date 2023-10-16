from App.database import db
from datetime import datetime

DEFAULT_RENTAL_PEROID = 14

class Rental(db.Model):
    rentalId = db.Column(db.Integer, primary_key=True)
    listingId = db.Column(db.Integer, db.ForeignKey('listing.listingId'))
    renterId = db.Column(db.Integer, db.ForeignKey('customer.id'))
    rental_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, default=None)
    payments = db.relationship('RentalPayment', backref=db.backref('rental', lazy='joined'))

    def __init__(self, renterId, listingId):
        self.renterId = renterId
        self.listingId = listingId
    
    def __repr__(self):
        return f'<rental {self.rentalId} owner: {self.listing.owner.username} renter: {self.renter.username} listingId: {self.listing.listingId} game: {self.listing.game.title}, returned: { self.return_date != None }>'
    
    def calculate_late_fees(self):
        days_rented = self.return_date - self.rental_date
        if days_rented.days <= DEFAULT_RENTAL_PEROID:
            return 0
        days_late = days_rented.days - DEFAULT_RENTAL_PEROID
        return  0.10 * self.listing.price * days_late 

    def return_rental(self):
         self.return_date = datetime.utcnow()
         fees = self.calculate_late_fees()
         self.listing.status = 'available'
         db.session.add(self)
         db.session.add(self.listing)
         db.session.commit()
         return fees
         

    def toJSON(self):
        return{
            'rentalId': self.rentalId,
            'listingId': self.listingId,
            'renterId': self.renterId,
            'rental_date': self.rental_date.strftime("%Y/%m/%d, %H:%M:%S"),
            'return_date': self.return_date.strftime("%Y/%m/%d, %H:%M:%S") if self.return_date else None
        }