from App.database import db
from datetime import datetime

class Payment(db.Model):
    paymentId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)

    def __init__(self, userId, amount):
        self.userId = userId
        self.amount = amount
