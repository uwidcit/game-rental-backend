from App.database import db
from App.models import Payment
from datetime import datetime

class RentalPayment(Payment):
    rentalId = db.Column(db.Integer, db.ForeignKey('rental.rentalId'))

    def __init__(self, rentalId, userId, amount):
        self.rentalId = rentalId
        self.userId = userId
        self.amount = amount


    def __repr__(self):
        return '<RentalPayment %r>' % self.id