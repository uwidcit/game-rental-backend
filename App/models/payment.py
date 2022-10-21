from App.database import db
from datetime import datetime

class Payment(db.Model):
    paymentId = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customer.id'))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)

    def __init__(self, customerId, amount):
        self.customerId = customerId
        self.amount = amount
    
    def toJSON():
        return {
            'paymentId': self.paymentId,
            'customerId': self.customerId,
            'payment_date': self.payment_date.strftime("%Y/%m/%d, %H:%M:%S"),
            'amount': self.amount
        }
