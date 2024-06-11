from .user import User
from App.database import db

class Customer(User):
    __tablename__ = 'customer'
    status = db.Column(db.String(120), nullable=False, default='active')
    listings = db.relationship('Listing', backref=db.backref('owner', lazy='joined'))
    rentals = db.relationship('Rental', backref=db.backref('renter', lazy='joined'))
    payments = db.relationship('Payment', backref=db.backref('customer', lazy='joined'))
    __mapper_args__ = {
      'polymorphic_identity': 'customer',
    }

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.user_type = "customer"

    def toJSON(self):
        return{
            'id': self.id,
            'username': self.username,
            'type': 'customer',
            'status': self.status
        }