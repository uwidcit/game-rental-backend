from App.database import db
from .payment import Payment
from .listing import Listing
from datetime import datetime

class RentalPayment(Payment):
    rentalId = db.Column(db.Integer, db.ForeignKey('rental.rentalId'))

    def __init__(self, rental):
        self.rentalId = rental.rentalId
        self.customerId = rental.renterId
        listing = Listing.query.get(rental.listingId)
        self.amount = listing.price


    def __repr__(self):
        return '<RentalPayment %r>' % self.paymentId
    
    def toJSON():
        return {
            'paymentId': self.paymentId,
            'customerId': self.customerId,
            'rentalId': self.rentalId,
            'payment_date': self.payment_date.strftime("%Y/%m/%d, %H:%M:%S"),
            'amount': self.amount
        }